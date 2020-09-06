from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Chapter
from .models import Book
from .models import Section
from .utils import custom_render, book_header
from . import forms
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from pyarticle.component.book_component import BookComponent
from django.http.response import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import uuid
import base64
# Create your views here.


@login_required(login_url='login/')
def add_section(request, book_id, chapter_id):
    bc = BookComponent(book_id)
    if not bc.is_my_book(request.user):
        raise Http404("不正なリクエストです")

    items = Section.objects.filter(chapter=chapter_id).aggregate(Max('order'))
    if 'order__max' in items:
        order_max = items['order__max'] + 1
    else:
        order_max = 1

    section_form = forms.SectionForm(initial={'text': "記事を書きます",
                                              'order': order_max})
    new_section_image_form = forms.SectionImageForm()

    data = {'section_form': section_form, 'section_image_datas': [],
            'new_section_image_form': new_section_image_form,
            'book_id': book_id, 'chapter_id': chapter_id, 'section_id': 0}

    return book_header(request, 'pyarticle/admin/section/section.html', bc, data)


@login_required(login_url='login/')
def edit_section(request, book_id, chapter_id, section_id):
    bc = BookComponent(book_id)
    if not bc.is_my_book(request.user):
        raise Http404("不正なリクエストです")

    record = Section.objects.get(id=section_id)
    if record.text == "":
        record.text = "ここに記事を書きます"
    section_form = forms.SectionForm(initial={'text': record.text,
                                              'order': record.order})

    data = {'section_form': section_form,
            'book_id': book_id, 'chapter_id': chapter_id, 'section_id': section_id}

    return book_header(request, 'pyarticle/admin/section/section.html', bc, data)


@login_required(login_url='login/')
def save_section(request, book_id, chapter_id, section_id):
    bc = BookComponent(book_id)
    if not bc.is_my_book(request.user):
        raise Http404("不正なリクエストです")

    if request.method == 'POST':
        bc = BookComponent(book_id)
        form = forms.SectionForm(request.POST)
        if form.is_valid():
            if section_id == 0:
                section_id = bc.create_section(chapter_id, form.cleaned_data['text'], form.cleaned_data['order'])
            else:
                bc.update_section(section_id, chapter_id, form.cleaned_data['text'], form.cleaned_data['order'])

        page = bc.get_page(section_id)
        return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))


@login_required(login_url='login/')
def delete_section(request, book_id, chapter_id, section_id):
    bc = BookComponent(book_id)
    if not bc.is_my_book(request.user):
        raise Http404("不正なリクエストです")

    # 現在のページ取得
    page = bc.get_page(section_id)
    # セクションを削除する
    bc.delete_section(section_id)

    if not bc.is_exists_chapter_section(chapter_id):
        # チャプターのセクションがすべて削除されたときは空のセクションを自動的に作成する
        new_section_id = bc.create_section(chapter_id, "記事を書きます", 1)
        page = bc.get_page(new_section_id)
    else:
        total_page = bc.get_page_count()
        if total_page < page:
            page = total_page

    return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))


@login_required(login_url='login/')
def upload_image(request):
    """
    この関数はセクションにあるべきではない
    """
    if request.method == 'POST':
        b = request.POST['image']
        tokens = b.split(",")
        header = tokens[0]
        ext = header.split(";")[0].split("/")[-1]

        img_data = base64.b64decode(tokens[1])
        # 画像ファイルに変換する
        prefix = 'media/section/'
        name = str(uuid.uuid4()).replace('-', '')
        filename = prefix + name + "." + ext

        with open(filename, "wb") as f:
            f.write(img_data)

    return JsonResponse({"filename": filename})
