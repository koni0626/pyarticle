from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'pyarticle/account/signup.html', {'form': form})


def logout(request):
    logout(request)
    return redirect('index')