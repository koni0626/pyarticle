import json
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .models import Chapter
from .models import Book
from .models import Section
from .utils import custom_render, book_header
from . import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from pyarticle.component.book_component import BookComponent
from django.http.response import JsonResponse, Http404
from django.db import DatabaseError, transaction
# Create your views here.


@login_required(login_url='login/')
def index(request, book_id):
    # チャプターの一覧を表示する
    book = Book.objects.get(id=book_id)
    chapter_records = Chapter.objects.filter(book=book)
    data = {'chapter_records': chapter_records, 'book_id': book_id}
    return custom_render(request, 'pyarticle/admin/chapter/index.html', data)


@login_required(login_url='login/')
def add_chapter(request, book_id):
    bc = BookComponent(book_id)
    if not bc.is_my_book(request.user):
        raise Http404("不正なリクエストです")

    # チャプターのorderの最大値を求める
    order_max = Chapter.objects.filter(book=book_id).aggregate(Max('order'))
    if 'order__max' in order_max:
        order_max = order_max['order__max'] + 1
    else:
        order_max = 1

    form = forms.ChapterForm(initial={'order': order_max})
    data = {'chapter_form': form, 'book_id': book_id, 'chapter_id': 0}
    return book_header(request, 'pyarticle/admin/chapter/chapter.html', bc, data)


@login_required(login_url='login/')
def edit_chapter(request, book_id, chapter_id):
    bc = BookComponent(book_id)
    if not bc.is_my_book(request.user):
        raise Http404("不正なリクエストです")

    record = Chapter.objects.get(id=chapter_id)
    form = forms.ChapterForm(initial={'chapter': record.chapter,
                                      'order': record.order})
    section_records = Section.objects.filter(chapter=Chapter.objects.get(id=chapter_id))
    data = {'chapter_form': form, 'section_records': section_records, 'book_id': book_id, 'chapter_id': chapter_id}
    return book_header(request, 'pyarticle/admin/chapter/chapter.html', bc, data)


@login_required(login_url='login/')
def delete_chapter(request, book_id, chapter_id):
    bc = BookComponent(book_id)
    if not bc.is_my_book(request.user):
        raise Http404("不正なリクエストです")

    bc.delete_chapter(chapter_id)
    page = 1
    if not bc.is_exists_chapters():
        # チャプターをすべて削除すると、ページがなくなってしまうので
        # 空のページを生成する
        bc.create_empty_book()

    return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))

@login_required(login_url='login/')
def save_chapter(request, book_id, chapter_id):
    if request.method == 'POST':
        bc = BookComponent(book_id)
        if not bc.is_my_book(request.user):
            raise Http404("不正なリクエストです")

        form = forms.ChapterForm(request.POST)
        if form.is_valid():
            if chapter_id == 0:
                chapter = Chapter(chapter=form.cleaned_data['chapter'],
                                  order=form.cleaned_data['order'],
                                  book=Book.objects.get(id=book_id))
                chapter.save()
                section = Section(text="",
                                  order=1,
                                  update_date=timezone.now(),
                                  chapter=Chapter.objects.get(id=chapter.id))
                section.save()
                page = bc.get_page(section.id)
                return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))
            else:
                chapter = Chapter.objects.get(id=chapter_id)
                chapter.chapter = form.cleaned_data['chapter']
                chapter.order = form.cleaned_data['order']
                chapter.book = Book.objects.get(id=book_id)
                chapter.save()
                #section_id = request.session['section_id']
                page = bc.get_chapter_top_page(chapter_id)
            return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))

@login_required(login_url='login/')
def upper_chapter(request, book_id, chapter_id, page):
    # チャプターを上下を入れ替える
    bc = BookComponent(book_id)
    if not bc.is_my_book(request.user):
        raise Http404("不正なリクエストです")

    bc.swap_chapter(chapter_id, True)

    return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))

@login_required(login_url='login/')
def under_chapter(request, book_id, chapter_id, page):
    # チャプターを上下を入れ替える
    bc = BookComponent(book_id)
    if not bc.is_my_book(request.user):
        raise Http404("不正なリクエストです")

    bc.swap_chapter(chapter_id, False)

    return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))

@login_required(login_url='login/')
def ajax_save_chapter(request):
    if request.method == 'POST':
        chapter_list = request.POST.get('chapter_list', None)
        book_id = request.POST.get('book_id', None)
        bc = BookComponent(book_id)
        if not bc.is_my_book(request.user):
            ret = {"result": -1, "message": "不正な値です"}
        else:
            chapter_list = json.loads(chapter_list)
            try:
                with transaction.atomic():
                    for i, html_chapter_id in enumerate(chapter_list):
                        chapter_id = html_chapter_id.split("_")[0]
                        bc.update_chapter_order(chapter_id, i+1)

                ret = {"result": 0, "message": "正常"}
            except DatabaseError:
                ret = {"result": -1, "message": "DBの更新に失敗しました"}
            else:
                ret = {"result": -1, "message": "不正な値です"}

    return JsonResponse(ret)
