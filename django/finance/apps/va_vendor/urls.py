from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"va_vendor", MainViewSet, basename="va_vendor")

urlpatterns = [
    path("", include(router.urls)),
]
