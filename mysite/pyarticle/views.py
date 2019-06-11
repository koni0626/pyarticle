from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Book
from .models import Chapter
from .models import Section
from .utils import custom_render


def index(request):
    records = Book.objects.all().order_by('id').reverse()

    for record in records:
        if len(record.description) > 10:
            record.description = record.description[0:100]
    return custom_render(request, 'pyarticle/index.html', {'book_records': records})


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


def book(request, book_id, chapter_id, page_number):
    book = Book.objects.get(id=book_id)
    try:
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
        sections = Section.objects.filter(chapter=chapter).order_by('order')
    except Section.DoesNotExist:
        raise Http404("Question does not exist")

    # sction_idがページ番号にすり替わっている。
    page_obj = paginate_query(request, sections, page_number, 1)
    section_id = 0
    for page in page_obj:
        page.access_count += 1
        section_id = page.id
        page.save()

    next_chapter_id = 0
    next_chapters = Chapter.objects.filter(book=book).order_by('order')
    for i, next_chapter in enumerate(next_chapters):
        print(chapter_id)
        if next_chapter.id == chapter_id:
            print("見つけた")
            if i < len(next_chapters) - 1:
                next_chapter_id = next_chapters[i + 1].id
                break

    data = {'book': book, 'chapters': chapters, 'chapter': chapter,
            'page_obj': page_obj, 'next_chapter_id': next_chapter_id}

    request.session['book_id'] = book.id
    request.session['chapter_id'] = chapter.id
    request.session['section_id'] = section_id
    request.session['page_number'] = page_number
    return custom_render(request, 'pyarticle/book.html', data)

