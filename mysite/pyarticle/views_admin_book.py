from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Book
from .models import Chapter
from .models import Section
from .utils import custom_admin_render
from . import forms
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def index(request):
    records = Book.objects.order_by('id').reverse().all()
    data = {
            'description': '書籍一覧',
            'book_records': records}
    return custom_admin_render(request, 'pyarticle/admin/book/index.html', data)


@login_required
def add_book(request):
    form = forms.BookForm(request.POST)
    return custom_admin_render(request, 'pyarticle/admin/book/book.html', {'book_form': form, 'book_id': 0})


@login_required
def edit_book(request, book_id):
    book_record = Book.objects.get(id=book_id)
    form = forms.BookForm(initial={'title': book_record.title,
                                   'author': book_record.author,
                                   'description': book_record.description,
                                   'category': book_record.category,
                                   'image': book_record.image})

    book = Book.objects.get(id=book_id)
    records = Chapter.objects.filter(book=book).order_by('order')
    data = {'book': book_record,
            'book_form': form,
            'book_id': book_id,
            'chapter_records': records,
            'book_id': book_id}

    return custom_admin_render(request, 'pyarticle/admin/book/book.html', data)


@login_required
def save_book(request, book_id):
    if request.method == 'POST':
        form = forms.BookForm(request.POST, request.FILES)
        if form.is_valid():
            if book_id == 0:
                # 新規投稿
                book = Book(title=form.cleaned_data['title'],
                            author=form.cleaned_data['author'],
                            description=form.cleaned_data['description'],
                            category=form.cleaned_data['category'])
                if form.cleaned_data['image']:
                    book.image = form.cleaned_data['image']
                else:
                    book.image = "cover/noimage.jpg"
                book.save()

                chapter = Chapter(order=1,
                                  book=Book.objects.get(id=book.id))
                chapter.save()

                section = Section(text="",
                              order=1,
                              chapter=Chapter.objects.get(id=chapter.id))
                section.save()
            else:
                book = Book.objects.get(id=book_id)
                book.title = form.cleaned_data['title']
                book.author = form.cleaned_data['author']
                book.description = form.cleaned_data['description']
                book.category = form.cleaned_data['category']
                #book.image = form.cleaned_data['image']
                if form.cleaned_data['image']:
                    book.image = form.cleaned_data['image']
                else:
                    if form.cleaned_data['image'] == False:
                        book.image = "cover/noimage.jpg"
                book.save()
        else:
            print("error＝＝＝＝＝＝＝")
            #return HttpResponseRedirect("/pyarticle/admin/book")
        return HttpResponseRedirect(reverse('index'))


@login_required
def delete_book(request, book_id):
    record = Book.objects.filter(id=book_id).delete()
    return HttpResponseRedirect(reverse('index'))
