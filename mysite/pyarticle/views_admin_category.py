from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Category
from .models import Chapter
from .utils import custom_render
from . import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import JsonResponse
from django.db.utils import IntegrityError
# Create your views here.


@login_required
def index(request):
    records = Category.objects.order_by('id').reverse().all()
    data = {
            'description': 'カテゴリー一覧',
            'category_records': records}
    return custom_render(request, 'pyarticle/admin/category/index.html', data)


@login_required
def add_category(request):
    form = forms.CategoryForm(request.POST)
    return custom_render(request, 'pyarticle/admin/category/category.html', {'category_form': form, 'category_id': 0})


@login_required
def edit_category(request, category_id):
    record = Category.objects.get(id=category_id)
    form = forms.CategoryForm(initial={'category': record.category_name})

    category = Category.objects.get(id=category_id)
    data = {'category_form': form,
            'category_id': category_id}

    return custom_render(request, 'pyarticle/admin/category/category.html', data)


@login_required
def save_category(request, category_id):
    if request.method == 'POST':
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            if category_id == 0:
                category = Category(category_name=form.cleaned_data['category'])
            else:
                category = Category.objects.get(id=category_id)
                category.category_name = form.cleaned_data['category']

            category.save()
        else:
            pass
            #return HttpResponseRedirect("/pyarticle/admin/book")
        return HttpResponseRedirect(reverse('category'))


@user_passes_test(lambda u: u.is_superuser)
def delete_category(request, category_id):
    record = Category.objects.filter(id=category_id).delete()
    return HttpResponseRedirect(reverse('category'))

@login_required
def ajax_save_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category', None)

        if len(category_name) > 0 and len(category_name) < 255:
            category = Category(category_name=category_name)
            try:
                category.save()
                ret = {"result": 0, "category_name": category_name, "id": category.id}
            except IntegrityError:
                ret = {"result": -1, "message": "{}はすでに登録されています".format(category_name)}
            except:
                ret = {"result": -1, "message": "カテゴリの登録に失敗しました"}

        elif len(category_name) == 0:
            ret = {"result": -1, "message": "カテゴリ名を入力してください"}
        elif len(category_name) > 255:
            ret = {"result": -1, "message": "カテゴリを255文字以内で指定してください"}
        else:
            ret = {"result": -1, "message": "不正な値です"}

    return JsonResponse(ret)
