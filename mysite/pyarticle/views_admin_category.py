from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Category
from .models import Chapter
from .utils import custom_admin_render
from . import forms
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def index(request):
    records = Category.objects.order_by('id').reverse().all()
    data = {
            'description': 'カテゴリー一覧',
            'category_records': records}
    return custom_admin_render(request, 'pyarticle/admin/category/index.html', data)


@login_required
def add_category(request):
    form = forms.CategoryForm(request.POST)
    return custom_admin_render(request, 'pyarticle/admin/category/category.html', {'category_form': form, 'category_id': 0})


@login_required
def edit_category(request, category_id):
    record = Category.objects.get(id=category_id)
    form = forms.CategoryForm(initial={'category': record.category_name})

    category = Category.objects.get(id=category_id)
    data = {'category_form': form,
            'category_id': category_id}

    return custom_admin_render(request, 'pyarticle/admin/category/category.html', data)


@login_required
def save_category(request, category_id):
    print("save_vategory")
    if request.method == 'POST':
        print("POST")
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            if category_id == 0:
                print(form.cleaned_data['category'])
                category = Category(category_name=form.cleaned_data['category'])
                print("bbb")
            else:
                category = Category.objects.get(id=category_id)

            category.save()
        else:
            print("valid")
            #return HttpResponseRedirect("/pyarticle/admin/book")
        return HttpResponseRedirect(reverse('category'))


@login_required
def delete_category(request, category_id):
    record = Category.objects.filter(id=category_id).delete()
    return HttpResponseRedirect(reverse('category'))
