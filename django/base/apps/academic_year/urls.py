from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"academic_year", MainViewSet, basename="academic_year")

urlpatterns = [
    path("", include(router.urls)),
]
