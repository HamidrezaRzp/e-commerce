from rest_framework.routers import DefaultRouter
from .views import ProductViewset

app_name = 'products'

router = DefaultRouter()
router.register('products', ProductViewset, basename='products')

urlpatterns = router.urls


