from django.http import HttpResponseRedirect
from django.urls import reverse
from pyarticle.models import Book
from pyarticle.models import Category
from pyarticle.models import Chapter
from pyarticle.models import Section
from pyarticle.utils import custom_render
from pyarticle.component.book_component import BookComponent
from pyarticle.utils import search_books
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from .forms import AttachFileForm
import glob
import os

"""
登録されている本一覧をカテゴリごとに表示する
"""
#@login_required(login_url='login/')
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

#@login_required(login_url='login/')
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
#@login_required(login_url='login/')
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

    # 添付ファイルのフォーム
    attach_file_form = AttachFileForm()
    path = 'media/attach/{}/*'.format(book_id)
    attach_file_list = []
    file_list = glob.glob(path)
    for file in file_list:
        filename = file.split(os.sep)[-1]
        attach_file_list.append(['/media/attach/{}/{}'.format(book_id, filename), filename])

    data = {'book': bc.book, 'chapter': chapter, 'chapter_list': chapter_list,
            'attach_file_form': attach_file_form,
            'prev_page': page-1,  'section': section, 'next_page': page+1,
            'total_page': total_page, 'now_page': page, 'attach_file_list': attach_file_list}

    return custom_render(request, 'pyarticle/book.html', data)

#@login_required(login_url='login/')
def chapter(request, book_id, chapter_id):
    bc = BookComponent(book_id)
    page = bc.get_chapter_top_page(chapter_id)

    return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))

def test(request):
    return custom_render(request, 'pyarticle/test.html',{"data":"だだだ"})