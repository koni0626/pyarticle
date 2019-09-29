from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Chapter
from .models import Book
from .models import Section
from .models import SectionImage
from .utils import custom_admin_render
from . import forms
from django.db.models import Max
from django.contrib.auth.decorators import login_required
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

    return custom_admin_render(request, 'pyarticle/admin/section/section.html', data)


@login_required
def edit_section(request, book_id, chapter_id, section_id):
    record = Section.objects.get(id=section_id)
    if record.text == "":
        record.text = "ここに記事を書きます"
    section_form = forms.SectionForm(initial={'text': record.text,
                                              'order': record.order})
    new_section_image_form = forms.SectionImageForm()
    section_image_datas = []
    try:
        section_images = SectionImage.objects.filter(section_id=section_id)

        for section_image in section_images:
            print(section_image.image.url)
            print(section_image.id)
            form = forms.SectionImageForm(initial={'image': section_image.image})
            section_image_datas.append({"form": form, "image": section_image})
    except SectionImage.DoesNotExist:
        print("レコードない")

    data = {'section_form': section_form, 'section_image_datas': section_image_datas,
            'new_section_image_form': new_section_image_form,
            'book_id': book_id, 'chapter_id': chapter_id, 'section_id': section_id}

    return custom_admin_render(request, 'pyarticle/admin/section/section.html', data)


@login_required
def save_section_image(request, book_id, chapter_id, section_id, image_id):
    if request.method == 'POST':
        # 画像を保存
        form = forms.SectionImageForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['image']:
                try:
                    section = Section.objects.get(id=section_id)
                except Section.DoesNotExist:
                    items = Section.objects.filter(chapter_id=chapter_id).aggregate(order_max=Max('order'))
                    order_max = items['order_max'] + 1
                    section = Section(text="記事を書きます",
                                      order=order_max,
                                      chapter=Chapter.objects.get(id=chapter_id))
                    section.save()
                    section_id = section.id

                if image_id == 0:
                    section_image = SectionImage(image=form.cleaned_data['image'],
                                                 section=section)
                else:
                    section_image = SectionImage(id=image_id,
                                                 image=form.cleaned_data['image'],
                                                 section=section)
                section_image.save()

        return HttpResponseRedirect(reverse('edit_section', args=[book_id, chapter_id, section_id]))


@login_required
def save_section(request, book_id, chapter_id, section_id):
    if request.method == 'POST':
        form = forms.SectionForm(request.POST)
        if form.is_valid():
            if section_id == 0:
                section = Section(text=form.cleaned_data['text'],
                                  order=form.cleaned_data['order'],
                                  chapter=Chapter.objects.get(id=chapter_id))
                section.save()
            else:
                section = Section.objects.get(id=section_id)
                section.text = form.cleaned_data['text']
                section.order = form.cleaned_data['order']
                section.chapter = Chapter.objects.get(id=chapter_id)
                section.save()

            return HttpResponseRedirect(reverse('disp_book', args=[book_id, chapter_id, section_id]))


@login_required
def delete_section(request, book_id, chapter_id, section_id):
    sections = Section.objects.filter(chapter_id=chapter_id)
    page_number = 0
    before_section_id = 0

    for p, sec in enumerate(sections):
        if sec.order == section_id:
            page_number = p + 1
            break
        before_section_id = sec.id

    Section.objects.filter(id=section_id).delete()

    return HttpResponseRedirect(reverse('disp_book', args=[book_id, chapter_id, before_section_id]))



