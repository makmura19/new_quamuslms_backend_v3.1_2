from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"tap_activity", MainViewSet, basename="tap_activity")

urlpatterns = [
    path("", include(router.urls)),
]
