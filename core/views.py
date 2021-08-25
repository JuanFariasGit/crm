from math import fsum

from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login as app_login,
    logout as app_logout
)
from django.contrib import messages

from product.models import Product
from provider.models import Provider
from stock_entry.models import StockEntry
from stock_exit.models import StockExit
from store.models import Store

from ultils.ultils import currency_format, porcent_format


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
    total_product = Product.objects.filter(user=request.user).aggregate(qt=Count('item'))
    total_provider = Provider.objects.filter(user=request.user).aggregate(qt=Count('company'))
    total_store = Store.objects.filter(user=request.user).aggregate(qt=Count('store'))
    total_product_entry_of_stock = StockEntry.objects.filter(user=request.user).\
        aggregate(qt=Coalesce(Sum('quantity'), 0))
    total_product_exit_of_stock = StockExit.objects.filter(user=request.user).\
        aggregate(qt=Coalesce(Sum('quantity'), 0))

    total_product_in_stock = total_product_entry_of_stock['qt'] - total_product_exit_of_stock['qt']
    total_revenue = fsum([p.quantity * p.price_unit for p in StockExit.objects.filter(user=request.user).all()])
    total_cost = fsum([p.quantity * p.cost_unit for p in StockEntry.objects.filter(user=request.user).all()])
    total_profit = total_revenue - total_cost
    profit_margin = total_profit / total_revenue if total_revenue != 0 else 0

    return render(request, 'core/index.html', {
        'total_product': total_product['qt'],
        'total_provider': total_provider['qt'],
        'total_store': total_store['qt'],
        'total_product_in_stock': total_product_in_stock,
        'total_revenue': currency_format(total_revenue),
        'total_cost': currency_format(total_cost),
        'total_profit': currency_format(total_profit),
        'profit_margin': porcent_format(profit_margin)
    })


def inventory(request):
    return render(request, 'core/inventory.html')
