from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login as app_login,
    logout as app_logout
)
from django.contrib import messages


def login(request):
    return render(request, 'core/login.html')


def verify_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            app_login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuário e/ou senha inválidos')
    return redirect('login')


def logout(request):
    app_logout(request)
    return redirect('/')


def dashboard(request):
    return render(request, 'core/index.html')


def inventory(request):
    return render(request, 'core/inventory.html')
