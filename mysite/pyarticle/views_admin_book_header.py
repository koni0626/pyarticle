from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .component.book_component import BookComponent
from .models import SiteParams
from .utils import custom_render, book_header, get_user
from . import forms
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def edit_header(request, book_id):
    user = get_user(request.user)
    request.session['book_header_url'] = request.META['HTTP_REFERER']
    try:
        bc = BookComponent(book_id)
        site_image = bc.header_image
        form = forms.SiteBookHeaderForm(initial={'image': site_image})

        data = {'header_form': form, 'site_image': site_image.url, 'book_id':book_id}
    except:
        form = forms.SiteBookHeaderForm()
        data = {'header_form': form, 'site_image': "", 'book_id': book_id}

    return book_header(request, 'pyarticle/admin/book_header/title.html', bc, data)


@login_required
def save_header_image(request, book_id):
    if request.method == 'POST':
        bc = BookComponent(book_id)
        form = forms.SiteBookHeaderForm(request.POST, request.FILES)
        if form.is_valid():

            if form.cleaned_data['image']:
                #bc.book.header_image = form.cleaned_data['image']
                bc.save_header(form.cleaned_data['image'])

        else:
            data = {'title_form': form, 'site_image': ""}
            return HttpResponseRedirect(request.session['book_header_url'])

        return HttpResponseRedirect(request.session['book_header_url'])
