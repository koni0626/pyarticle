from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.urls import reverse
from pyarticle.models import Book, AccessLog
from pyarticle.models import Category
from pyarticle.models import Chapter
from pyarticle.models import Section
from pyarticle.utils import custom_render, book_header
from pyarticle.component.book_component import BookComponent
from pyarticle.utils import search_books
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from .forms import AttachFileForm
import glob
import os


# @login_required(login_url='login/')
def index(request):
    # マイページには自分の投稿記事とプロフィールを表示する
    book_records = Book.objects.order_by('create_date').reverse().all()
    # 本全体のアクセス数をカウントする
    books = []
    for book in book_records:
        bc = BookComponent(book.id)
        if bc.draft == 1:
            books.append(bc.book_info())

    # 検索フォームの作成
    search_form = SearchForm()

    # 人気記事top10
    popular_books = []
    popular_records = Book.objects.order_by('good_count').reverse().all()[:10]
    for book in popular_records:
        bc = BookComponent(book.id)
        if bc.draft == 1:
            popular_books.append(bc.book_info())

    data = {'books': books, 'search_form': search_form, 'popular_books': popular_books}
    return custom_render(request, 'pyarticle/index.html', data)


# @login_required(login_url='login/')
def index_old(request):
    """
    登録されている本一覧をカテゴリごとに表示する
    :param request:
    :return:なし
    """
    # 検索フォームの作成
    search_form = SearchForm()
    # カテゴリの取得
    categories = Category.objects.all().order_by('category_name')
    records = {}
    for category in categories:
        book_records = Book.objects.filter(category=category).order_by('id').reverse()
        if len(book_records) == 0:
            continue
        records[category.category_name] = []

        # カテゴリごとに本をまとめる
        for book_record in book_records:
            bc = BookComponent(book_record.id)
            acc = bc.get_book_access_count()
            if len(book_record.description) > 10:
                book_record.description = book_record.description[0:100]

            first_chapter = Chapter.objects.filter(book=book_record).order_by('order').first()
            first_section = Section.objects.filter(chapter=first_chapter).order_by('order').first()
            records[category.category_name].append([book_record, acc, first_chapter, first_section])

    return custom_render(request, 'pyarticle/index.html', {'book_records': records, 'search_form': search_form})


# @login_required(login_url='login/')
def search(request):
    """
    本を検索する
    :param request:
    :return:
    """
    results = []
    # 検索窓には、検索したときの文字を表示したい
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            key_word = search_form.cleaned_data['key_word']
            results = search_books(key_word)
    else:
        search_form = SearchForm()

    data = {'search_form': search_form,
            'results': results}

    return custom_render(request, 'pyarticle/book_search.html', data)


# @login_required(login_url='login/')
def book(request, book_id, page):
    """
    本を表示する
    :param request:
    :param book_id:
    :param page:
    :return:
    """
    """
    if 'HTTP_REFERER' in request.META:
        print(request.META['HTTP_REFERER'])
        print(request.META['REMOTE_ADDR'])
        print(request.META['OS'])
        print(request.META['HTTP_USER_AGENT'])

        for meta in request.META:
            print("{}/{}".format(meta,request.META[meta]))
    else:
        print("ありません")
    """
    bc = BookComponent(book_id)

    if not bc.is_my_book(request.user):
        is_my_page = False
        print("私のページではありません")
    else:
        is_my_page = True
        print("私のページです")

    bc = BookComponent(book_id)
    if (not is_my_page) and (bc.draft == 0):
        raise Http404("不正なリクエストです")

    total_page = bc.get_page_count()
    if total_page == 0:
        # ページが一個もなかったら空のページを作成する
        bc.create_empty_book()
        total_page = bc.get_page_count()

    # セクションのアクセス数を更新して保存する
    bc.update_access_count(request, page)
    # アクセス数を取得する
    acc = bc.get_book_access_count()

    # ナビゲーション用データの作成
    top_chapter_list = bc.get_chapter_list()
    chapter_list = []
    for chapter_record in top_chapter_list:
        # セクションのうち、見出し1で始まるものを取得する
        sub_chapter_list = bc.get_chapter_in_section(chapter_record)
        chapter_list.append([chapter_record, sub_chapter_list])

    chapter_record, section_record = bc.get_chapter_and_section(page)
    _, prev_section = bc.get_chapter_and_section(page - 1)
    _, next_section = bc.get_chapter_and_section(page + 1)

    # 添付ファイル一覧
    attach_file_list = bc.get_attach_list()

    # ユーザが★を押しているかどうか
    is_press_good = bc.is_already_good(request)
    if is_press_good:
        good_image = 'star_on.png'
    else:
        good_image = 'star_off.png'

    data = {'book': bc.book, 'chapter': chapter_record, 'chapter_list': chapter_list,
            'attach_file_form': bc.attach_file_form, 'comment_form': bc.comment_form, 'acc': acc,
            'prev_page': page - 1, 'section': section_record, 'next_page': page + 1,
            'total_page': total_page, 'now_page': page, 'attach_file_list': attach_file_list,
            'profile': bc.profile, 'is_my_page': is_my_page, 'good_image': good_image}

    access_log = AccessLog()
    access_log.write_log(request, bc.book.user, bc.book, chapter_record, section_record)

    return book_header(request, 'pyarticle/book.html', bc, data)


# @login_required(login_url='login/')
def chapter(request, book_id, chapter_id):
    bc = BookComponent(book_id)
    page = bc.get_chapter_top_page(chapter_id)

    return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))


def set_good(request, book_id):
    """★をクリックしたとき"""
    bc = BookComponent(book_id)
    bc.set_good(request)
    count = bc.get_book_good_count()
    return JsonResponse({'good_count': count})
