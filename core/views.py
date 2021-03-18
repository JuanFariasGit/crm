from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as app_login, logout as app_logout
from django.contrib import messages
from product.models import Product
from provider.models import Provider
from store.models import Store
from stock_entry.models import StockEntry
from stock_exit.models import StockExit
from django.http import JsonResponse


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


def inventory(request):
  return render(request, 'core/inventory.html')


def get_quantity_product_in_stock(id):
  return StockEntry.get_number_of_product_entries(id) - StockExit.get_number_of_product_exit(id)


def get_total_profit(id):
  return StockExit.get_total_revenue_by_id(id) - StockEntry.get_total_cost_by_id(id)


def get_status(id):
  qt_product_in_stock = get_quantity_product_in_stock(id)
  product = Product.objects.get(id=id)
  qt_min = product.level_minimum
  qt_max = product.level_maximum
  if qt_product_in_stock == 0:
    return '<p class="bg-danger text-white rounded">Sem Estoque</p>'
  elif qt_product_in_stock < qt_min or qt_product_in_stock > qt_max:
    return '<p class="bg-info text-white rounded">Estoque Perigoso</p>'
  else:
    return '<p class="bg-success text-white rounded">Estoque Confortável</p>'


def get_data_inventory(request):
  products = Product.objects.all()
  response = {"data":
    [
      {
        "DT_RowId":f"row_{product.id}",
        "Produto":product.item,
        "Entradas":StockEntry.get_number_of_product_entries(product.id),
        "Saídas":StockExit.get_number_of_product_exit(product.id),
        "Estoque Atual":get_quantity_product_in_stock(product.id),
        "Estoque Mínimo":product.level_minimum,
        "Estoque Máximo":product.level_maximum,
        "Status":get_status(product.id),
        "Receita Total":f'R$ {StockExit.get_total_revenue_by_id(product.id):.2f}'.replace(".",","),
        "Custo Total":f'R$ {StockEntry.get_total_cost_by_id(product.id):.2f}'.replace(".",","),
        "Lucro":f'R$ {get_total_profit(product.id):.2f}'.replace(".",",")
      }

      for product in products
    ]
  }
  return JsonResponse(response)