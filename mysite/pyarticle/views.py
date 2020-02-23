from django.http import HttpResponseRedirect
from django.urls import reverse
from pyarticle.models import Book
from pyarticle.models import Category
from pyarticle.models import Chapter
from pyarticle.models import Section
from pyarticle.utils import custom_render
from pyarticle.component.book_component import BookComponent
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from django.db.models import Q

"""
登録されている本一覧をカテゴリごとに表示する
"""
@login_required(login_url='login/')
def index(request):
    search_form = SearchForm()

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

    return custom_render(request, 'pyarticle/index.html', {'book_records': records, 'search_form':search_form})


def search_books(key_word):
    results = [] # score, 見つかった文字列, 本のID, ページ番号

    book_records = Book.objects.filter(title__contains=key_word)
    if len(book_records) > 0:
        for record in book_records:
            results.append({'score': 10, 'title': record.title, 'text': record.description, 'book_id': record.id, 'page':1})

    book_records = Book.objects.filter(description__contains=key_word)
    if len(book_records) > 0:
        for record in book_records:
            results.append({'score': 8, 'title': record.title, 'text': record.description, 'book_id': record.id, 'page': 1})


    chapter_records = Chapter.objects.filter(chapter__contains=key_word)
    if len(chapter_records) > 0:
        for record in chapter_records:
            book_id = record.book.id
            bc = BookComponent(book_id)
            page = bc.get_chapter_top_page(record.id)
            results.append({'score': 5, 'title': bc.title, 'text': record.chapter, 'book_id': book_id, 'page': page})

    section_records = Section.objects.filter(text__contains=key_word)
    if len(section_records) > 0:
        for record in section_records:
            book_id = record.chapter.book.id
            bc = BookComponent(book_id)
            page = bc.get_page(record.id)
            results.append({'score': 3, 'title': bc.title, 'text': record.text, 'book_id': book_id, 'page': page})

    return results


@login_required(login_url='login/')
def search(request):
    '''
    検索機能
    :param request:
    :return:
    '''
    results = []
    # 検索窓には、検索したときの文字を表示したい
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            key_word = search_form.cleaned_data['key_word']
            results = search_books(key_word)
            print(results)
    else:
        search_form = SearchForm()

    data = {'search_form': search_form,
            'results': results}

    return custom_render(request, 'pyarticle/book_search.html', data)

"""
本を表示する
"""
@login_required(login_url='login/')
def book(request, book_id, page):
    bc = BookComponent(book_id)
    total_page = bc.get_page_count()
    if total_page == 0:
        # ページが一個もなかったら空のページを作成する
        bc.create_empty_book()

    chapter_list = bc.get_chapter_list()
    chapter, section = bc.get_chapter_and_section(page)
    _, prev_section = bc.get_chapter_and_section(page - 1)
    _, next_section = bc.get_chapter_and_section(page + 1)

    data = {'book': bc.book, 'chapter': chapter, 'chapter_list': chapter_list,
            'prev_page': page-1,  'section': section, 'next_page': page+1,
            'total_page': total_page, 'now_page': page}

    return custom_render(request, 'pyarticle/book.html', data)

@login_required(login_url='login/')
def chapter(request, book_id, chapter_id):
    bc = BookComponent(book_id)
    page = bc.get_chapter_top_page(chapter_id)

    return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))

def test(request):
    return custom_render(request, 'pyarticle/test.html',{"data":"だだだ"})