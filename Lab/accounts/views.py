from re import template
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import *
from .forms import OrderForm, CustomerForm, ProductForm
from .serializers import ProductSerializer, CustomerSerializer, OrderSerializer
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework import generics, status
import requests

# Create your views here.
class ProductViewSet(viewsets.ViewSet):
    
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def retrieve(self, request, pk=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(products)
        return Response(serializer.data)

    def update(self, request):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    def destroy(self, request):
        product = Product.objects.get(id=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerViewSet(viewsets.ViewSet):
    
    def list(self, request):
        customer = Customer.objects.all()
        serializer = CustomerSerializer(customer, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def retrieve(self, request, pk=None):
        customer = Customer.objects.get(id=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def update(self, request):
        customer = Customer.objects.get(id=pk)
        serializer = ProductSerializer(instance=customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    def destroy(self, request):
        customer = Customer.objects.get(id=pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'customers':customers, 'total_orders':total_orders, 'total_customers':total_customers, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/dashboard.html', context)
'''
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'customers': CustomerSerializer(customers, many=True).data, 'total_orders':total_orders, 'total_customers':total_customers, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/dashboard.html', context)

'''
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})
'''

def products(request):
    assert isinstance(request, HttpRequest)
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    print(serializer.data)
    return render(request, 'accounts/products.html', {'products': serializer.data},)

'''
def customers(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer':customer, 'orders':orders, 'order_count':order_count}
    return render(request, 'accounts/customers.html', context)
'''
def customers(request, pk_test):
    assert isinstance(request, HttpRequest)
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    current_customer = Customer.objects.filter(id=pk_test)
    order_count = orders.count()
    context = {'customer':CustomerSerializer(current_customer, many=True).data, 'orders':orders, 'order_count':order_count, 'customer_id': pk_test}
    return render(request, 'accounts/customers.html', context)


def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #print('Printing POST: ', request.POST)
        form = OrderForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        #print('Printing POST: ', request.POST)
        form = OrderForm(request.POST, instance=order)
        if(form.is_valid()):
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'accounts/delete.html', context)

def createCustomer(request):
    form = CustomerForm()
    if(request.method == 'POST'):
        form = CustomerForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/customer_form.html', context)

def createCustomer(request):
    customer = get_object_or_404(Customer)
    serializer = CustomerSerializer(customer)
    if serializer.is_valid():
        return Response({{'serializer': serializer, 'customer': customer}})
    serializer.save()
    return redirect('/')

def createProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/products/')

    context = {'form':form}
    return render(request, 'accounts/product_form.html', context)
