from django.contrib import admin
from .models import Cart, CartItme

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['user', 'created_at']
    ordering = ('created_at','updated_at',)


@admin.register(CartItme)
class CartItmeAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product','quantity']
    list_filter = ['cart']
    search_fields = ['cart']
    ordering = ('cart',)