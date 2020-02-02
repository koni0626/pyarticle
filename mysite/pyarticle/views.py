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


def book(request, book_id, page):

    bc = BookComponent(request, book_id)
    total_page = bc.total_page
    chapter_list = bc.get_chapter_list()
    chapter, section = bc.get_page(page)

    _, prev_section = bc.get_page(page - 1)
    _, next_section = bc.get_page(page + 1)

    data = {'book': bc.book, 'chapter': chapter, 'chapter_list': chapter_list,
            'prev_page': page-1,  'section': section, 'next_page': page+1,
            'total_page': total_page, 'now_page': page}
    print(data)
    return custom_render(request, 'pyarticle/book.html', data)

