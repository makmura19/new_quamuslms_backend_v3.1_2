from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"practice_variant", MainViewSet, basename="practice_variant")

urlpatterns = [
    path("", include(router.urls)),
]
