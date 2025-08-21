from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"dormitory_room", MainViewSet, basename="dormitory_room")

urlpatterns = [
    path("", include(router.urls)),
]
