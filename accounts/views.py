from django.shortcuts import render
from django.http import HttpResponse
from accounts.models import *

# Create your views here.
def home(request):
    # return HttpResponse('Home')
    return render(request, 'accounts/dashboard.html')

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {
        'products': products
    })

def customer(request):
    # return HttpResponse('Customer')
    return render(request, 'accounts/customer.html')