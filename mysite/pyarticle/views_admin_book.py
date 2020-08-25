from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import timezone

from .component.book_component import BookComponent
from .models import Book
from .models import Chapter
from .models import Section
from .utils import custom_render
from . import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import base64
import uuid
import os

# Create your views here.


@login_required
def index(request):
    records = Book.objects.order_by('id').reverse().all()
    data = {
            'description': '書籍一覧',
            'book_records': records}
    return custom_render(request, 'pyarticle/admin/book/index.html', data)


@login_required
def add_book(request):
    book_form = forms.BookForm(request.POST)
    category_form = forms.CategoryForm(request.POST)

    data = {'book_form': book_form, 'book_id': 0,'category_form': category_form}
    return custom_render(request, 'pyarticle/admin/book/book.html', data)


@login_required
def edit_book(request, book_id):
    bc = BookComponent(book_id)
    if not bc.is_my_book(request.user):
        raise Http404("不正なリクエストです")

    book_record = Book.objects.get(id=book_id)
    form = forms.BookForm(initial={'title': book_record.title,
                                   'description': book_record.description,
                                   'category': book_record.category,
                                   'image': book_record.image,
                                   'footer': book_record.footer})

    book = Book.objects.get(id=book_id)
    records = Chapter.objects.filter(book=book).order_by('order')
    data = {'book': book_record,
            'book_form': form,
            'book_id': book_id,
            'chapter_records': records,
            'book_id': book_id}

    return custom_render(request, 'pyarticle/admin/book/book.html', data)


@login_required
def edit_footer(request, book_id, section_id):
    bc = BookComponent(book_id)
    form = forms.FooterForm(initial={'footer': bc.book.footer})
    data = {'footer_form': form, 'book_id': book_id, 'section_id': section_id}

    return custom_render(request, 'pyarticle/admin/book/footer.html', data)


@login_required
def save_footer(request, book_id, section_id):
    if request.method == 'POST':
        form = forms.FooterForm(request.POST)
        if form.is_valid():
            book = Book.objects.get(id=book_id)
            book.footer = form.cleaned_data['footer']
            book.save()

    bc = BookComponent(book_id)
    page = bc.get_page(section_id)
    return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))


@login_required
def save_book(request, book_id):
    if request.method == 'POST':
        form = forms.BookForm(request.POST, request.FILES)
        if form.is_valid():
            if book_id == 0:
                # 新規投稿
                book = Book(title=form.cleaned_data['title'],
                            user=request.user,
                            description=form.cleaned_data['description'],
                            category=form.cleaned_data['category'],
                            footer=form.cleaned_data['footer'])

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
                #book.image = form.cleaned_data['image']
                book.footer = form.cleaned_data['footer']
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


@login_required
def delete_book(request, book_id):
    bc = BookComponent(book_id)
    if not bc.is_my_book(request.user):
        raise Http404("不正なリクエストです")

    record = Book.objects.filter(id=book_id).delete()
    return HttpResponseRedirect(reverse('my_page'))

@login_required
def upload_attach_file(request, book_id, page):
    """
    この関数はセクションにあるべきではない
    """
    save_path = 'attach/{}'.format(book_id)
    bc = BookComponent(book_id)
    if not bc.is_my_book(request.user):
        raise Http404("不正なリクエストです")

    if request.method == 'POST' and request.FILES['attach_file']:
        attach_file = request.FILES['attach_file']
        fileobject = FileSystemStorage()
        file_path = os.path.join(save_path, attach_file.name)
        file_data = fileobject.save(file_path, attach_file)
        attach_file_name = settings.MEDIA_ROOT + '/attach/{}/{}'.format(book_id, attach_file.name)
        os.chmod(attach_file_name, 0o666)
        upload_url = fileobject.url(file_data)
    else:
        pass

    return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))


@login_required
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

