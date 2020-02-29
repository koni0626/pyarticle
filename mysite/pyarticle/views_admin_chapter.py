from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Chapter
from .models import Book
from .models import Section
from .utils import custom_render
from . import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from pyarticle.component.book_component import BookComponent
# Create your views here.


@login_required
def index(request, book_id):
    # チャプターの一覧を表示する
    book = Book.objects.get(id=book_id)
    print(book)
    chapter_records = Chapter.objects.filter(book=book)
    data = {'chapter_records': chapter_records, 'book_id': book_id}
    return custom_render(request, 'pyarticle/admin/chapter/index.html', data)


@login_required
def add_chapter(request, book_id):
    # チャプターのorderの最大値を求める
    order_max = Chapter.objects.filter(book=book_id).aggregate(Max('order'))
    print(order_max)
    if 'order__max' in order_max:
        order_max = order_max['order__max'] + 1
    else:
        order_max = 1

    form = forms.ChapterForm(initial={'order': order_max})
    data = {'chapter_form': form, 'book_id': book_id, 'chapter_id': 0}
    return custom_render(request, 'pyarticle/admin/chapter/chapter.html', data)


@login_required
def edit_chapter(request, book_id, chapter_id):
    record = Chapter.objects.get(id=chapter_id)
    form = forms.ChapterForm(initial={'chapter': record.chapter,
                                      'order': record.order})
    section_records = Section.objects.filter(chapter=Chapter.objects.get(id=chapter_id))
    data = {'chapter_form': form, 'section_records': section_records, 'book_id': book_id, 'chapter_id': chapter_id}
    return custom_render(request, 'pyarticle/admin/chapter/chapter.html', data)


@login_required
def delete_chapter(request, book_id, chapter_id):
    bc = BookComponent(book_id)
    bc.delete_chapter(chapter_id)
    page = 1
    if not bc.is_exists_chapters():
        # チャプターをすべて削除すると、ページがなくなってしまうので
        # 空のページを生成する
        bc.create_empty_book()

    return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))

@login_required
def save_chapter(request, book_id, chapter_id):
    if request.method == 'POST':
        bc = BookComponent(book_id)
        form = forms.ChapterForm(request.POST)
        if form.is_valid():
            if chapter_id == 0:
                chapter = Chapter(chapter=form.cleaned_data['chapter'],
                                  order=form.cleaned_data['order'],
                                  book=Book.objects.get(id=book_id))
                chapter.save()
                section = Section(text="",
                                  order=1,
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

@login_required
def upper_chapter(request, book_id, chapter_id, page):
    # チャプターを上下を入れ替える
    bc = BookComponent(book_id)
    bc.swap_chapter(chapter_id, True)

    return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))

@login_required
def under_chapter(request, book_id, chapter_id, page):
    # チャプターを上下を入れ替える
    bc = BookComponent(book_id)
    bc.swap_chapter(chapter_id, False)

    return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))
