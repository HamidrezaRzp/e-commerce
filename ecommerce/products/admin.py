from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Product, Category, Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock']
    list_filter = ['category']
    search_fields = ['name', 'category']
    ordering = ('created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    list_filter = ['name']
    search_fields = ['name',]
    ordering = ('name','created_at',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'score']
    list_filter = ['product', 'user']
    search_fields = ['product', 'user']
    ordering = ('created_at','updated_at',)
