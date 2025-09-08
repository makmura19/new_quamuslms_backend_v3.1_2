from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"invoice_price_variant", MainViewSet, basename="invoice_price_variant")

urlpatterns = [
    path("", include(router.urls)),
]
