from rest_framework import serializers
from .models import Product, Category, Review
from django.db.models import Avg


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["user", "rating", "comment", "created_at"]


class ProductSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    recent_reviews = serializers.SerializerMethodField()
    seller = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Product
        fields = ['name',
                  'description',
                  'category',
                  'price',
                  'stock',
                  'seller',
                  'average_rating',
                  'recent_reviews']
    
    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(avg=Avg('ratings'))['avg']
        return round(avg, 2) if avg else None
    
    def get_recent_reviews(self, obj):
        reviews = obj.reviews.select_related('user').order_by('created_at')[:3]
        return ReviewSerializer(reviews, many=True).data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

