# tracker/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TransactionViewSet, InvestmentViewSet

router = DefaultRouter()
router.register("categories",   CategoryViewSet)
router.register("transactions", TransactionViewSet)
router.register("investments",  InvestmentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]