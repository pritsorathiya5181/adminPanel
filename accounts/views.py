from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from accounts.models import *
from .forms import OrderFrom
from .filters import OrderFilter

# Create your views here.
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    context = {
        "orders": orders,
        "customers": customers,
        "total_orders": total_orders,
        "delivered": delivered,
        "pending": pending,
    }
    # return HttpResponse('Home')
    return render(request, "accounts/dashboard.html", context)


def products(request):
    products = Product.objects.all()
    return render(request, "accounts/products.html", {"products": products})


def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()

    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs
    
    context = { 
        "customer": customer, 
        "orders": orders, 
        "order_count": order_count,
        "myfilter": myfilter
    }
    # return HttpResponse('Customer')
    return render(request, "accounts/customer.html", context)


def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=("product", "status"), extra=5
    )
    customer = Customer.objects.get(id=pk)
    # form = OrderFrom(initial={'customer': customer})
    formSet = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == "POST":
        print("Printing POST request:", request.POST)
        # form = OrderFrom(request.POST)
        formSet = OrderFormSet(request.POST, instance=customer)
        if formSet.is_valid():
            formSet.save()
            return redirect("/")

    context = {"formSet": formSet}
    return render(request, "accounts/orders_form.html", context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    formSet = OrderFrom(instance=order)

    if request.method == "POST":
        print("Printing POST request:", request.POST)
        formSet = OrderFrom(request.POST, instance=order)
        if formSet.is_valid():
            formSet.save()
            return redirect("/")

    context = {"formSet": formSet}
    return render(request, "accounts/orders_form.html", context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect("/")

    context = {"item": order}
    return render(request, "accounts/delete.html", context)

