from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"nano_external_id", MainViewSet, basename="nano_external_id")

urlpatterns = [
    path("", include(router.urls)),
]
