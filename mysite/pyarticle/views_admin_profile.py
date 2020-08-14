from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Category, User
from .models import Profile
from .utils import custom_render, get_user
from . import forms
from django.contrib.auth.decorators import login_required
import traceback
# Create your views here.


@login_required
def edit(request):
    user = get_user(request.user)

    try:
        profile_record = Profile.objects.filter(user=user).first()
    except Exception as e:
        print(traceback.format_exc())
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

            profile_record.image = form.cleaned_data['image']
            profile_record.site = form.cleaned_data['site']
            profile_record.belong = form.cleaned_data['belong']
            profile_record.intro = form.cleaned_data['intro']
            profile_record.twitter = form.cleaned_data['twitter']
            profile_record.user = user
            profile_record.save()

            output = {'profile_form': form, 'profile': profile_record}
        else:
            raise Http404("不正なリクエストです(4)")
    else:
        raise Http404("不正なリクエストです(5)")

    return custom_render(request, 'pyarticle/admin/profile/edit.html', output)
