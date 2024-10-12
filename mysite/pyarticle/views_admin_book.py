import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from .component.book_component import BookComponent
from .component.media_component import change_attach_file_permission
from .models import Book
from .models import Chapter
from .models import Section
from .utils import custom_render
from . import forms

# Create your views here.


@require_http_methods(['GET'])
@login_required(login_url='login/')
def add_book(request):
    """
    マイページで本を追加を選択した場合
    :param request: リクエスト
    :return:
    """
    # 本を追加するフォームを作成する
    book_form = forms.BookForm(request.POST)

    # カテゴリ一覧を入力するフォームを作成する
    category_form = forms.CategoryForm(request.POST)

    # カテゴリを新規追加する場合、book_idは0にする。
    data = {'book_form': book_form,
            'book_id': 0,
            'category_form': category_form}

    return custom_render(request, 'pyarticle/admin/book/book.html', data)


@require_http_methods(['GET'])
@login_required(login_url='login/')
def edit_book(request, book_id):
    """
    本を編集する
    :param request: リクエスト
    :param book_id: 編集する本のID
    :return:
    """
    bc = BookComponent(book_id)
    if not bc.is_my_book(request.user):
        raise Http404("不正なリクエストです")

    book_record = Book.objects.get(id=book_id)
    form = forms.BookForm(initial={'title': book_record.title,
                                   'description': book_record.description,
                                   'category': book_record.category,
                                   'image': book_record.image,
                                   'footer': book_record.footer,
                                   'draft': book_record.draft})

    book = Book.objects.get(id=book_id)
    records = Chapter.objects.filter(book=book).order_by('order')
    data = {'book': book_record,
            'book_form': form,
            'book_id': book_id,
            'chapter_records': records,
            'book_id': book_id}

    return custom_render(request, 'pyarticle/admin/book/book.html', data)


@require_http_methods(['GET'])
@login_required(login_url='login/')
def edit_footer(request, book_id, section_id):
    """
    本のフッターを編集する
    :param request: リクエスト
    :param book_id: 本のID
    :param section_id: セクションID
    :return:
    """
    bc = BookComponent(book_id)
    # フッター編集用のフォームを作成する
    form = forms.FooterForm(initial={'footer': bc.book.footer})
    data = {'footer_form': form, 'book_id': book_id, 'section_id': section_id}

    return custom_render(request, 'pyarticle/admin/book/footer.html', data)


@require_http_methods(['POST'])
@login_required(login_url='login/')
def save_footer(request, book_id, section_id):
    """
    フッターを保存する。
    :param request: リクエスト
    :param book_id: 本のID
    :param section_id: セクションのID 編集後、前のページに戻るために使用する
    :return:
    """
    if request.method == 'POST':
        form = forms.FooterForm(request.POST)
        if form.is_valid():
            book = Book.objects.get(id=book_id)
            book.footer = form.cleaned_data['footer']
            book.save()

    bc = BookComponent(book_id)
    page = bc.get_page(section_id)
    return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))


@require_http_methods(['POST', 'PUT'])
@login_required(login_url='login/')
def save_book(request, book_id):
    """
    本を保存する
    :param request: リクエスト
    :param book_id: 本のID
    :return:
    """
    if request.method == 'POST':
        form = forms.BookForm(request.POST, request.FILES)
        if form.is_valid():
            if book_id == 0:
                # 新規投稿
                book = Book(title=form.cleaned_data['title'],
                            user=request.user,
                            description=form.cleaned_data['description'],
                            category=form.cleaned_data['category'],
                            footer=form.cleaned_data['footer'],
                            draft=form.cleaned_data['draft'],
                            article_type=form.cleaned_data['article_type'])

                if form.cleaned_data['image']:
                    if form.cleaned_data['image'] is not False:
                        book.image = form.cleaned_data['image']
                    else:
                        book.image = None

                book.save()

                chapter = Chapter(order=1,
                                  book=Book.objects.get(id=book.id))
                chapter.save()

                section = Section(text="",
                              order=1,
                              update_date=timezone.now(),
                              chapter=Chapter.objects.get(id=chapter.id))
                section.save()
            else:
                book = Book.objects.get(id=book_id)
                book.title = form.cleaned_data['title']
                book.description = form.cleaned_data['description']
                book.category = form.cleaned_data['category']
                book.footer = form.cleaned_data['footer']
                book.draft = form.cleaned_data['draft']
                book.article_type = form.cleaned_data['article_type']
                if form.cleaned_data['image']:
                    book.image = form.cleaned_data['image']
                else:
                    if form.cleaned_data['image'] is False:
                        book.image = None
                book.save()
        else:
            pass
            #return HttpResponseRedirect("/pyarticle/admin/book")
        return HttpResponseRedirect(reverse('my_page'))


@require_http_methods(['POST', 'PUT', 'DELETE'])
@login_required(login_url='login/')
def delete_book(request, book_id):
    """
    本を削除する
    :param request:
    :param book_id:
    :return:
    """
    bc = BookComponent(book_id)
    if not bc.is_my_book(request.user):
        raise Http404("不正なリクエストです")

    record = Book.objects.filter(id=book_id).delete()
    return HttpResponseRedirect(reverse('my_page'))


@login_required(login_url='login/')
def upload_attach_file(request, book_id, page):
    """
    添付ファイルを付ける
    :param request: リクエスト
    :param book_id: 添付する本のID
    :param page: ページ番号
    :return:
    """

    bc = BookComponent(book_id)
    if not bc.is_my_book(request.user):
        raise Http404("不正なリクエストです")

    # 添付ファイルの保存先を取得する
    save_path = bc.get_attach_path()

    if request.method == 'POST' and request.FILES['attach_file']:
        # ファイルを保存する
        attach_file = request.FILES['attach_file']
        # TODO 許可するファイルの拡張子を決めたほうがいいかも
        fileobject = FileSystemStorage()
        file_path = os.path.join(save_path, attach_file.name)
        fileobject.save(file_path, attach_file)
        # ファイルの権限を変更する
        change_attach_file_permission(book_id, attach_file.name)

    return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))


@require_http_methods(['POST', 'PUT'])
@login_required(login_url='login/')
def delete_attach_file(request, book_id, page, filename):
    bc = BookComponent(book_id)
    if not bc.is_my_book(request.user):
        raise Http404("不正なリクエストです")

    attach_file_name = settings.MEDIA_ROOT + '/attach/{}/{}'.format(book_id, filename)
    if os.path.exists(attach_file_name):
        os.remove(attach_file_name)
    else:
        pass

    return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))

