from django.urls import path
from .views import ProductViewSet, CustomerViewSet
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    #path('products/', views.products, name="products"),
    path('customers/<str:pk_test>/', views.customers, name="customer"),
    path('create_order/<str:pk>/', views.createOrder, name="createOrder"),
    path('update_order/<str:pk>', views.updateOrder, name="updateOrder"),
    path('delete/<str:pk>', views.deleteOrder, name="deleteOrder"),
    path('create_customer/', views.createCustomer, name="createCustomer"),
    path('create_product/', views.createProduct, name="createProduct"),
    #path('products/api', views.product_api, name="products_api"),
    
    path('products/api', ProductViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('products/api/<str:pk>', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('customers/api', CustomerViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('customers/api/<str:pk>', CustomerViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),

]