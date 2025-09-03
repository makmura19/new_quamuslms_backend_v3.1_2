from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.user_service import UserService
from constants.access import Role, SCHOOL_ROLES
from models.res_user import ResUser, ResUserData
from models.authentication_user import AuthenticationUserData
from rest_framework.exceptions import AuthenticationFailed
from helpers.user_service import UserService
from rest_framework.exceptions import ValidationError
import os


class MainService(BaseService):
    @staticmethod
    def superadmin(model: ResUser, validated_data, extra, user, headers_dict=None):
        from django.conf import settings

        user_data = ResUser().find_one({"authority_codes": Role.SUPERADMIN.value})
        if user_data:
            raise ValidationError("Superadmin is exists")

        new_user_data = ResUserData(
            name="Superadmin",
            login=settings.SUPERADMIN_USERNAME,
            password="****",
            is_staff_admin=True,
            is_staff=True,
            authority_codes=[Role.SUPERADMIN.value],
        )
        new_auth_data = AuthenticationUserData(
            username=settings.SUPERADMIN_USERNAME,
            password=settings.SUPERADMIN_PASSWORD,
            role=Role.SUPERADMIN.value,
            school_code="quamus",
            is_staff=True,
        )
        result = model.insert_one(new_user_data)
        UserService().create_user(new_auth_data)
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }

    @staticmethod
    def login(model: BaseModel, validated_data, extra, user, headers_dict=None):
        user = UserService.login(validated_data)
        if not user.is_company_active:
            raise AuthenticationFailed("Login Gagal, Company ID tidak aktif.")
        access = user.tokens().get("access")
        refresh = user.tokens().get("refresh")
        return {
            "access": access,
            "refresh": refresh,
            "user": MainService.get_profile(user),
        }

    @staticmethod
    def change_password(
        model: BaseModel, validated_data, extra, user, headers_dict=None
    ):
        res_user = ResUser()
        user = UserService.change_password(
            user.username,
            validated_data.get("old_password"),
            validated_data.get("new_password"),
        )
        update_data = {"is_hashed": True, "password": user.password}
        res_user.update_one(
            {"login": user.username}, update_data=update_data, user=user
        )
        return {
            "data": {},
            "message": None,
        }

    @staticmethod
    def me(model: BaseModel, query_params, params_validation, user, headers_dict=None):
        user_data = MainService.get_profile(user)
        return {"data": {"user": user_data}, "metadata": []}

    @staticmethod
    def get_profile(user):
        import jwt
        from django.conf import settings
        from models.res_partner import ResPartner

        res_user = ResUser()
        res_partner = ResPartner()

        user_roles = user.role.split(",")
        if Role.SUPERADMIN in user_roles:
            user_data = {
                "name": "Superadmin",
                "username": user.username.split("_")[1],
                "authority": user_roles,
                "school_id": user.school_id,
                "holding_id": user.holding_id,
            }
        elif any(role in user_roles for role in SCHOOL_ROLES):
            from models.school_school import SchoolSchool
            from bson import ObjectId

            res_user_data = res_user.find_one(
                {"login": user.username}, convert_to_json=False
            )
            school_data = SchoolSchool().find_one({"_id": ObjectId(user.school_id)})
            user_data = {
                "name": res_user_data.get("name"),
                "username": user.username.split("_")[1],
                "authority": user_roles,
                "school_id": user.school_id,
                "school": {
                    "_id": school_data.get("_id"),
                    "name": school_data.get("name"),
                    "module_ids": school_data.get("module_ids"),
                    "module_codes": school_data.get("module_codes"),
                    "logo_md": school_data.get("logo_md"),
                },
            }
        else:
            res_user_data = res_user.find_one(
                {"login": user.username}, convert_to_json=False
            )
            user_data = {
                "name": res_user_data.get("name"),
                "username": res_user_data.get("login"),
                "authority": user.role.split(","),
                "school_id": user.school_id,
                "holding_id": user.holding_id,
            }

        user_jwt = jwt.encode(user_data, settings.SECRET_KEY, algorithm="HS256")
        if isinstance(user_jwt, bytes):
            user_jwt = user_jwt.decode("utf-8")
        return user_jwt
