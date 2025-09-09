from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"practice_rule", MainViewSet, basename="practice_rule")

urlpatterns = [
    path("", include(router.urls)),
]
