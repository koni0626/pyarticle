from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Chapter
from .models import Book
from .models import Section
from .utils import custom_admin_render
from . import forms
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def index(request, book_id):
    # チャプターの一覧を表示する
    book = Book.objects.get(id=book_id)
    print(book)
    chapter_records = Chapter.objects.filter(book=book)
    data = {'chapter_records': chapter_records, 'book_id': book_id}
    return custom_admin_render(request, 'pyarticle/admin/chapter/index.html', data)


@login_required
def add_chapter(request, book_id):
    form = forms.ChapterForm()
    data = {'chapter_form': form, 'book_id': book_id, 'chapter_id': 0}
    return custom_admin_render(request, 'pyarticle/admin/chapter/chapter.html', data)


@login_required
def edit_chapter(request, book_id, chapter_id):
    record = Chapter.objects.get(id=chapter_id)
    form = forms.ChapterForm(initial={'chapter': record.chapter,
                                      'order': record.order})
    section_records = Section.objects.filter(chapter=Chapter.objects.get(id=chapter_id))
    data = {'chapter_form': form, 'section_records': section_records, 'book_id': book_id, 'chapter_id': chapter_id}
    return custom_admin_render(request, 'pyarticle/admin/chapter/chapter.html', data)


@login_required
def save_chapter(request, book_id, chapter_id):
    if request.method == 'POST':
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
                return HttpResponseRedirect(reverse('disp_book', args=[book_id, chapter.id, section.id]))
            else:
                chapter = Chapter.objects.get(id=chapter_id)
                chapter.chapter = form.cleaned_data['chapter']
                chapter.order = form.cleaned_data['order']
                chapter.book = Book.objects.get(id=book_id)
                chapter.save()
                section_id = request.session['section_id']
            return HttpResponseRedirect(reverse('disp_book', args=[book_id, chapter.id, section_id]))

