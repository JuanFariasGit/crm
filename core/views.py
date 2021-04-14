from django.shortcuts import render, redirect
from django.contrib.auth import (
                                authenticate,
                                login as app_login,
                                logout as app_logout
                                )
from django.contrib import messages
from product.models import Product
from provider.models import Provider
from store.models import Store
from stock_entry.models import StockEntry
from stock_exit.models import StockExit
from django.http import JsonResponse
import math
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


def get_quantity_product_in_stock():
    entry = [entry.quantity for entry in StockEntry.objects.all()]
    exit = [exit.quantity for exit in StockExit.objects.all()]
    return int(math.fsum(entry)) - int(math.fsum(exit))


def dashboard(request):
    product_quantity = len(Product.objects.all())
    provider_quantity = len(Provider.objects.all())
    store_quantity = len(Store.objects.all())
    qt_product_total_in_stock = get_quantity_product_in_stock()
    total_revenue = StockExit.get_total_revenue()
    total_cost = StockEntry.get_total_cost()
    total_profit = total_revenue - total_cost
    profit_margin = (total_profit / total_revenue) if total_revenue != 0 else 0
    return render(request, 'core/index.html', {
          'product_quantity': product_quantity,
          'provider_quantity': provider_quantity,
          'store_quantity': store_quantity,
          'qt_product_total_in_stock': qt_product_total_in_stock,
          'total_revenue': currency_format(total_revenue),
          'total_cost': currency_format(total_cost),
          'total_profit': currency_format(total_profit),
          'profit_margin': porcent_format(profit_margin)
        }
    )


def inventory(request):
    return render(request, 'core/inventory.html')


def get_quantity_product_in_stock_by_id(id):
    entry = StockEntry.get_number_of_product_entries(id)
    exit = StockExit.get_number_of_product_exit(id)
    return entry - exit


def get_total_profit_by_id(id):
    revenue = StockExit.get_total_revenue_by_id(id)
    cost = StockEntry.get_total_cost_by_id(id)
    return revenue - cost


def get_status(id):
    qt_product_in_stock = get_quantity_product_in_stock_by_id(id)
    product = Product.objects.get(id=id)
    qt_min = product.level_minimum
    qt_max = product.level_maximum
    if qt_product_in_stock == 0:
        el = '<p class="bg-danger text-white rounded">Sem Estoque</p>'
    elif qt_product_in_stock < qt_min or qt_product_in_stock > qt_max:
        el = '<p class="bg-info text-white rounded">Estoque Perigoso</p>'
    else:
        el = '<p class="bg-success text-white rounded">Estoque Confortável</p>'
    return el


def get_data_inventory(request):
    products = Product.objects.all()
    response = {"data": [
        {
            "DT_RowId": f"row_{product.id}",
            "Produto": product.item,
            "Entradas": StockEntry.get_number_of_product_entries(product.id),
            "Saídas": StockExit.get_number_of_product_exit(product.id),
            "Estoque Atual": get_quantity_product_in_stock_by_id(product.id),
            "Estoque Mínimo": product.level_minimum,
            "Estoque Máximo": product.level_maximum,
            "Status": get_status(product.id),
            "Receita Total": currency_format(
                StockExit.get_total_revenue_by_id(product.id),
            ),
            "Custo Total": currency_format(
                StockEntry.get_total_cost_by_id(product.id),
            ),
            "Lucro": currency_format(get_total_profit_by_id(product.id))
        }

        for product in products
        ]
    }
    return JsonResponse(response)
