from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from users.forms import LoginUserForm, RegistrationForm


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Перенаправление на домашнюю страницу
    else:
        form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Создание пользователя
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)  # Авторизация после регистрации
            return redirect('/')  # Перенаправление на домашнюю страницу
    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('ad_list'))