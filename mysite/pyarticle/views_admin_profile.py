from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.urls import reverse
from .models import Category, User
from .models import Profile
from .utils import custom_render, get_user
from . import forms
from django.contrib.auth.decorators import login_required
import traceback
# Create your views here.


@login_required(login_url='login/')
def edit(request):
    user = get_user(request.user)

    try:
        profile_record = Profile.objects.filter(user=user).first()
        if profile_record is None:
            profile_record = Profile()
            #profile_record.image = "profile/noprofimg.png"
    except Exception as e:
        raise Http404("不正なリクエストです")

    if request.method == 'GET':
        if profile_record is not None:
            # すでにプロフィールが登録されている場合
            form = forms.ProfileForm(initial=profile_record.get_form_param())
        else:
            # まだプロフィールが新規登録されていない場合
            form = forms.ProfileForm()
        output = {'profile_form': form, 'profile': profile_record}

    elif request.method == 'POST':
        # 保存する場合
        form = forms.ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # profileを取得
            if profile_record is None:
                profile_record = Profile()
            if form.cleaned_data['image'] is not None:
                if form.cleaned_data['image'] is not False:
                    profile_record.image = form.cleaned_data['image']
                else:
                    profile_record.image = None

            profile_record.site = form.cleaned_data['site']
            profile_record.nem_address = form.cleaned_data['nem_address']
            profile_record.nem_message = form.cleaned_data['nem_message']
            profile_record.intro = form.cleaned_data['intro']
            profile_record.twitter = form.cleaned_data['twitter']
            profile_record.user = user
            profile_record.name = form.cleaned_data['name']

            profile_record.save()
            # 編集完了
            return redirect('my_page')
        else:
            raise Http404("不正なリクエストです(4)")
    else:
        raise Http404("不正なリクエストです(5)")

    return custom_render(request, 'pyarticle/admin/profile/edit.html', output)
