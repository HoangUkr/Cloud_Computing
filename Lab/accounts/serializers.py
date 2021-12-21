from django.db.models import fields
from .models import Product, Customer, Order
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField()
    product = serializers.ReadOnlyField()
    class Meta:
        model = Order
        fields = (
            'date_created',
            'status',
            'customer',
            'product'
        )