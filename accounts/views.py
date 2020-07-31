from django.shortcuts import render
from django.http import HttpResponse
from accounts.models import *

# Create your views here.
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }
    # return HttpResponse('Home')
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {
        'products': products
    })

def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    order = customer.order_set.all()
    order_count = order.count()
    context = {
        'customer': customer,
        'order': order,
        'order_count': order_count
    }
    # return HttpResponse('Customer')
    return render(request, 'accounts/customer.html', context)