from math import fsum

from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render

from apps.product.models import Product
from apps.provider.models import Provider
from apps.stock_entry.models import StockEntry
from apps.stock_exit.models import StockExit
from apps.store.models import Store

from apps.ultils.ultils import currency_format, porcent_format


def dashboard(request):
    total_product = Product.objects.filter(user=request.user).aggregate(qt=Count('item'))
    total_provider = Provider.objects.filter(user=request.user).aggregate(qt=Count('company'))
    total_store = Store.objects.filter(user=request.user).aggregate(qt=Count('store'))
    total_product_entry_of_stock = StockEntry.objects.filter(user=request.user).\
        aggregate(qt=Coalesce(Sum('quantity'), 0))
    total_product_exit_of_stock = StockExit.objects.filter(user=request.user).\
        aggregate(qt=Coalesce(Sum('quantity'), 0))

    total_product_in_stock = total_product_entry_of_stock['qt'] - total_product_exit_of_stock['qt']
    total_revenue = fsum([p.quantity * p.price_unit for p in StockExit.objects.filter(user=request.user)])
    total_cost = fsum([p.quantity * p.cost_unit for p in StockEntry.objects.filter(user=request.user)])
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


def inventory_data(request):
    products = Product.objects.filter(user=request.user)
    data = []
    for p in products:
        total_product_entry_of_stock = StockEntry.objects.filter(product__item=p.item, user=p.user). \
            aggregate(qt=Coalesce(Sum('quantity'), 0))
        total_product_exit_of_stock = StockExit.objects.filter(product__item=p.item, user=p.user). \
            aggregate(qt=Coalesce(Sum('quantity'), 0))
        total_product_in_stock = total_product_entry_of_stock['qt'] - total_product_exit_of_stock['qt']

        qt_min = p.level_minimum
        qt_max = p.level_maximum

        if total_product_in_stock == 0:
            status = '<p class="bg-danger text-white rounded">Sem Estoque</p>'
        elif total_product_in_stock < qt_min or total_product_in_stock > qt_max:
            status = '<p class="bg-warning text-white rounded">Estoque Perigoso</p>'
        else:
            status = '<p class="bg-success text-white rounded">Estoque Confortável</p>'

        data.append({
            "DT_RowId": f"row_{p.id}",
            "Produto": p.item,
            "Entradas": total_product_entry_of_stock['qt'],
            "Saídas": total_product_exit_of_stock['qt'],
            "Estoque Atual": total_product_in_stock,
            "Estoque Mínimo": qt_min,
            "Estoque Máximo": qt_max,
            "Status": status
        })

    return JsonResponse(data={'data': data}, status=200)
