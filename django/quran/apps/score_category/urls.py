from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"score_category", MainViewSet, basename="score_category")

urlpatterns = [
    path("", include(router.urls)),
]
