from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from models.authentication_user import AuthenticationUserData


class UserManager(BaseUserManager):

    def create_user(self, auth_data: AuthenticationUserData):
        user = self.model(
            school_id=auth_data.school_id,
            holding_id=auth_data.holding_id,
            school_code=auth_data.school_code,
            identity_number=auth_data.identity_number,
            username=auth_data.username,
            role=auth_data.role,
            is_company_active=auth_data.is_company_active,
        )
        user.set_password(auth_data.password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    school_id = models.CharField(max_length=255, default="")
    holding_id = models.CharField(max_length=255, default="")
    school_code = models.CharField(max_length=255, default="")
    identity_number = models.CharField(max_length=255, default="")
    username = models.CharField(max_length=255, unique=True, default=None)
    role = models.CharField(max_length=255, default="")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_company_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
