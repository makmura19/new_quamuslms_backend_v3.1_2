from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"mutabaah_group", MainViewSet, basename="mutabaah_group")

urlpatterns = [
    path("", include(router.urls)),
]
