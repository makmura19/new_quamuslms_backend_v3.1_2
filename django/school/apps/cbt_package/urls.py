from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"cbt_package", MainViewSet, basename="cbt_package")

urlpatterns = [
    path("", include(router.urls)),
]
