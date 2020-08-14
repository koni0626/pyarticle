from django.contrib import auth#auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from pyarticle.utils import custom_render
from django.contrib.auth import get_user_model
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='login/')
def signup(request):
    """
    サインアップでユーザ新規追加という意味らしい
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    return custom_render(request, 'pyarticle/account/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        #ここのフォームがcreate用のフォームになっている。
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()

    return custom_render(request, 'pyarticle/account/login.html', {'form': form})

@login_required(login_url='login/')
def logout(request):
    auth.logout(request)
    return redirect('index')