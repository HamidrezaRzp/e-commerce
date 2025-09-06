from .models import Product, Category
from .serializers import ProductSerializer
from rest_framework import viewsets
from .permissions import ProductPermissions
from rest_framework.response import Response
from users.utils import RedisJWTAuthentication

class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ProductPermissions]
    authentication_classes = [RedisJWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)