from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Chapter
from .models import Book
from .models import Section
from .utils import custom_render
from . import forms
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from pyarticle.component.book_component import BookComponent
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
import base64
# Create your views here.


@login_required
def add_section(request, book_id, chapter_id):
    items = Section.objects.filter(chapter_id=chapter_id).aggregate(order_max=Max('order'))
    print(items)
    if items['order_max'] == None:
        order_max = 1
    else:
        order_max = items['order_max'] + 1

    section_form = forms.SectionForm(initial={'text': "記事を書きます",
                                              'order': order_max})
    new_section_image_form = forms.SectionImageForm()

   # data = {'section_form': form, 'book_id': book_id, 'chapter_id': chapter_id, 'section_id': 0}
    data = {'section_form': section_form, 'section_image_datas': [],
            'new_section_image_form': new_section_image_form,
            'book_id': book_id, 'chapter_id': chapter_id, 'section_id': 0}

    return custom_render(request, 'pyarticle/admin/section/section.html', data)


@login_required
def edit_section(request, book_id, chapter_id, section_id):
    record = Section.objects.get(id=section_id)
    if record.text == "":
        record.text = "ここに記事を書きます"
    section_form = forms.SectionForm(initial={'text': record.text,
                                              'order': record.order})

    data = {'section_form': section_form,
            'book_id': book_id, 'chapter_id': chapter_id, 'section_id': section_id}

    return custom_render(request, 'pyarticle/admin/section/section.html', data)


@login_required
def save_section(request, book_id, chapter_id, section_id):
    if request.method == 'POST':
        bc = BookComponent(book_id)
        form = forms.SectionForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['text'])
            if section_id == 0:
                section_id = bc.create_section(chapter_id, form.cleaned_data['text'], form.cleaned_data['order'])
            else:
                bc.update_section(section_id, chapter_id, form.cleaned_data['text'], form.cleaned_data['order'])

        page = bc.get_page(section_id)
        return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))


@login_required
def delete_section(request, book_id, chapter_id, section_id):
    bc = BookComponent(book_id)
    # セクションを削除する
    bc.delete_section(section_id)

    if not bc.is_exists_chapter(chapter_id):
        # チャプターのセクションがすべて削除されたときは空のセクションを自動的に作成する
        new_section_id = bc.create_section(chapter_id, "記事を書きます", 1)
        page = bc.get_page(new_section_id)
    else:
        page = bc.get_page(section_id)
        page += 1

    return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))


@csrf_exempt
def upload_image(request):
    """
    この関数はセクションにあるべきではない
    """
    if request.method == 'POST':
        b = request.POST['image']
        tokens = b.split(",")
        header = tokens[0]
        ext = header.split(";")[0].split("/")[-1]
        print(ext)

        img_data = base64.b64decode(tokens[1])
        # 画像ファイルに変換する
        prefix = 'media/section/'
        name = str(uuid.uuid4()).replace('-', '')
        filename = prefix + name + "." + ext

        with open(filename, "wb") as f:
            f.write(img_data)

    return JsonResponse({"filename": filename})