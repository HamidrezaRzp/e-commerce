from .models import Product
from .serializers import ProductSerializer, ReviewSerializer
from rest_framework import viewsets
from .permissions import ProductPermissions
from users.utils import RedisJWTAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status



class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ProductPermissions]
    authentication_classes = [RedisJWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    @action(detail=True, methods=["get"])
    def reviews(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.select_related("user").all()
        page = self.paginate_queryset(reviews)

        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
