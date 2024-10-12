import traceback

from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

from .models import SiteParams, User
from .models import Book, Chapter, Section

from pyarticle.component.book_component import BookComponent
# Create your views here.


def custom_render(request, template, data=None):
    # サイトの名前と説明を毎回呼び出す。もっといい方法はないものか？

    site_name = SiteParams.objects.get(param='site_name').value
    description = SiteParams.objects.get(param='site_description').value
    image = SiteParams.objects.get(param='site_image').image
    try:
        url = image.url
    except:
        url = ""

    upload_url = SiteParams.objects.get(param='upload_url').value
    data_sitekey = SiteParams.objects.get(param='data_sitekey').value
    site_news = SiteParams.objects.get(param='site_news').value

    record = {'site_name': site_name, 'description': description, 'site_image': url,
              'upload_url': upload_url, 'data_sitekey': data_sitekey, 'site_news': site_news,
              'header': reverse('edit_title')}
    if data is not None:
        record.update(data)

    return render(request, template, record)


def book_header(request, template, book, data):
    # サイトの名前と説明を毎回呼び出す。もっといい方法はないものか？

    site_name = book.get_title()
    description = book.get_description()
    image = book.get_header_image()
    upload_url = SiteParams.objects.get(param='upload_url').value
    data_sitekey = SiteParams.objects.get(param='data_sitekey').value

    try:
        url = image.url
    except:
        url = ""

    header_url = reverse('my_book_header', args=[book.book_id])#+"/" + book.book_id
    record = {'site_name': site_name, 'description': description, 'site_image': url, 'upload_url': upload_url, 'data_sitekey': data_sitekey,
              'header': header_url}
    record.update(data)
    return render(request, template, record)


def search_books(key_word):
    results = [] # score, 見つかった文字列, 本のID, ページ番号

    book_records = Book.objects.filter(title__contains=key_word, draft=1)
    if len(book_records) > 0:
        for record in book_records:
            results.append({'score': 10, 'title': record.title, 'text': record.description, 'book_id': record.id, 'page':1})

    book_records = Book.objects.filter(description__contains=key_word, draft=1)
    if len(book_records) > 0:
        for record in book_records:
            results.append({'score': 8, 'title': record.title, 'text': record.description, 'book_id': record.id, 'page': 1})

    chapter_records = Chapter.objects.filter(chapter__contains=key_word)
    if len(chapter_records) > 0:
        for record in chapter_records:
            book_id = record.book.id
            bc = BookComponent(book_id)
            if bc.draft == 1:
                page = bc.get_chapter_top_page(record.id)
                results.append({'score': 5, 'title': bc.title, 'text': record.chapter, 'book_id': book_id, 'page': page})

    section_records = Section.objects.filter(text__contains=key_word)
    if len(section_records) > 0:
        for record in section_records:
            book_id = record.chapter.book.id
            bc = BookComponent(book_id)
            if bc.draft == 1:
                page = bc.get_page(record.id)
                results.append({'score': 3, 'title': bc.title, 'text': record.text, 'book_id': book_id, 'page': page})

    return results


def get_user(user):
    try:
        user = User.objects.filter(username=user).first()
        if user is None:
            raise Http404("不正なリクエストです")
    except:
        print(traceback.format_exc())
        raise Http404("不正なリクエストです")

    return user