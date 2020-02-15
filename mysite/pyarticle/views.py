from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from pyarticle.models import Book
from pyarticle.models import Category
from pyarticle.models import Chapter
from pyarticle.models import Section
from pyarticle.utils import custom_render
from pyarticle.component.book_component import BookComponent

"""
登録されている本一覧をカテゴリごとに表示する
"""
def index(request):
    categories = Category.objects.all().order_by('category_name')

    records = {}
    for category in categories:
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
本を表示する
"""
def book(request, book_id, page):
    bc = BookComponent(book_id)
    total_page = bc.get_page_count()
    chapter_list = bc.get_chapter_list()
    chapter, section = bc.get_chapter_and_section(page)
    _, prev_section = bc.get_chapter_and_section(page - 1)
    _, next_section = bc.get_chapter_and_section(page + 1)

    data = {'book': bc.book, 'chapter': chapter, 'chapter_list': chapter_list,
            'prev_page': page-1,  'section': section, 'next_page': page+1,
            'total_page': total_page, 'now_page': page}

    return custom_render(request, 'pyarticle/book.html', data)


def chapter(request, book_id, chapter_id):
    bc = BookComponent(book_id)
    page = bc.get_chapter_top_page(chapter_id)

    return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))

def test(request):
    return custom_render(request, 'pyarticle/test.html',{"data":"だだだ"})