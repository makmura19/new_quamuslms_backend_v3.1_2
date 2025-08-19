from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"program", MainViewSet, basename="program")

urlpatterns = [
    path("", include(router.urls)),
]
