from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"config_quran_report", MainViewSet, basename="config_quran_report")

urlpatterns = [
    path("", include(router.urls)),
]
