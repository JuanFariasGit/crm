from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as app_login, logout as app_logout
from django.contrib import messages
from product.models import Product
from provider.models import Provider
from store.models import Store
from stock_entry.models import StockEntry


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
  product_quantity = len(Product.objects.all()) 
  provider_quantity = len(Provider.objects.all())
  store_quantity = len(Store.objects.all())
  total_cost = StockEntry.get_total_cost()
  
  return render(request, 'core/index.html', 
    {
      'product_quantity': product_quantity,
      'provider_quantity': provider_quantity,
      'store_quantity': store_quantity,
      'total_cost': total_cost
    }
  )