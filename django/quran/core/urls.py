from django.urls import path, include
import os
from pathlib import Path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

BASE_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = BASE_DIR / "apps"
urlpatterns = [
    path("", include("user.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

for app_name in os.listdir(APPS_DIR):
    if app_name.startswith("_"):
        continue
    app_path = APPS_DIR / app_name
    if app_path.is_dir() and (app_path / "__init__.py").exists():
        urls_module = f"apps.{app_name}.urls"
        try:
            __import__(urls_module)
            urlpatterns.append(path("", include(urls_module)))
        except ModuleNotFoundError as e:
            print(e)
            continue
