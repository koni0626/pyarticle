from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Book
from .models import Category
from .models import Chapter
from .models import Section
from .utils import custom_render


def index(request):
    categorys = Category.objects.all().order_by('category_name')
    print(categorys)
    records = {}
    for category in categorys:
        books = Book.objects.filter(category=category).order_by('id').reverse()
        if len(books) == 0:
            continue
        records[category.category_name] = []

        for book in books:
            if len(book.description) > 10:
                book.description = book.description[0:100]

            first_chapter = Chapter.objects.filter(book=book).order_by('order').first()
            first_section = Section.objects.filter(chapter=first_chapter).order_by('order').first()
            records[category.category_name].append([book, first_chapter, first_section])

    return custom_render(request, 'pyarticle/index.html', {'book_records': records})


"""
使用していません
"""
def paginate_query(request, queryset, page_number, count):
    paginator = Paginator(queryset, count)
   # page = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


def book(request, book_id, chapter_id, section_id):

    # 本を検索する
    book = Book.objects.get(id=book_id)

    try:
        # チャプターを検索する
        chapters = Chapter.objects.filter(book=book).order_by('order')
        if len(chapters) == 0:
            raise Http404("not exist chapter")
        elif chapter_id == 0:
            chapter = chapters[0]
            chapter_id = chapter.id
        else:
            chapter = Chapter.objects.get(id=chapter_id)
            chapter.access_count += 1
            chapter.save()
    except Chapter.DoesNotExist:
        raise Http404("Question does not exist")


    try:
        # セクションを検索する
        chapter_list = []
       # first_sections = {}
        sections = None
        for chapter in chapters:
            #chapter_list.append(chapter.id) #本にあるチャプターすべてを取得
            chapter_sections = Section.objects.filter(chapter=chapter).order_by('order')
            if sections == None:
                sections = chapter_sections
            else:
                sections = sections | chapter_sections
            chapter_list.append([chapter, chapter_sections[0]])

    except Section.DoesNotExist:
        raise Http404("Question does not exist")

    # 現在表示するチャプターを検索する
    prev_chapter = None
    next_chapter = None
    for i, chapter in enumerate(chapters):
        if chapter_id == chapter.id:
            now_section = chapter
            page = i
            if i > 0:
                prev_chapter = chapters[i-1]
            if i+1 < len(chapters):
                next_chapter = chapters[i+1]
            break


    # 現在表示するセクションを検索する
    prev_section = None
    next_section = None
    now_page = 1
    for i, section in enumerate(sections):
        if section_id == section.id:
            if i > 0:
                prev_section = sections[i-1]
            if i+1 < len(sections):
                next_section = sections[i+1]
            now_page = i + 1
            break

    total_page = len(sections)
    data = {'book': book, 'chapter': chapter, 'chapter_list': chapter_list,
            'prev_section': prev_section,  'section': section, 'next_section': next_section,
            'total_page': total_page, 'now_page': now_page}

    return custom_render(request, 'pyarticle/book.html', data)

