from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"invoice_type", MainViewSet, basename="invoice_type")

urlpatterns = [
    path("", include(router.urls)),
]
