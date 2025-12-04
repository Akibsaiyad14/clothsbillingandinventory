from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClothItemViewSet, StockViewSet

router = DefaultRouter()
router.register(r'items', ClothItemViewSet)
router.register(r'stock', StockViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
