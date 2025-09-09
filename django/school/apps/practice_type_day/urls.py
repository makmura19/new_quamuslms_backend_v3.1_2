from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"practice_type_day", MainViewSet, basename="practice_type_day")

urlpatterns = [
    path("", include(router.urls)),
]
