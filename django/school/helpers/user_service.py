from user.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, ValidationError, AuthenticationFailed
import os
from django.contrib.auth.hashers import make_password
from models.authentication_user import AuthenticationUserData
from typing import List


class UserService:

    @staticmethod
    def create_user(auth_data: AuthenticationUserData):
        User.objects.create_user(auth_data)

    @staticmethod
    def create_superadmin():
        return User.objects.create_superuser(
            company_id=os.environ.get("SUPERADMIN_COMPANY"),
            email=os.environ.get("SUPERADMIN_email"),
            password=os.environ.get("SUPERADMIN_PASSWORD"),
        )

    @staticmethod
    def bulk_create_users(auth_data_list: List[AuthenticationUserData]):
        if not auth_data_list:
            raise ValidationError("auth_data_list tidak boleh kosong.")

        user_objects = []

        for auth_data in auth_data_list:
            user = User(
                school_id=auth_data.school_id,
                holding_id=auth_data.holding_id,
                school_code=auth_data.school_code,
                username=auth_data.username,
                role=auth_data.role,
                is_staff=auth_data.is_staff,
                is_active=auth_data.is_active,
                is_company_active=auth_data.is_company_active,
                password=make_password(auth_data.password),
            )
            user_objects.append(user)

        User.objects.bulk_create(user_objects)
        return {"created": len(user_objects)}

    @staticmethod
    def login(data):
        username = f"{data.get('code')}_{data.get('username')}"
        user = authenticate(username=username, password=data.get("password"))
        if not user:
            raise AuthenticationFailed("Invalid username or password.")
        return user

    @staticmethod
    def change_password(email, old_password, new_password):
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise NotFound("User not found.")

        if not user.check_password(old_password):
            raise ValidationError("Old password is incorrect.")

        user.set_password(new_password)
        user.save()
        return True

    @staticmethod
    def reset_password(email, new_password):
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise NotFound("User not found.")

        user.set_password(new_password)
        user.save()
        return True

    @staticmethod
    def verify_email(email):
        return User.objects.filter(email=email).exists()

    @staticmethod
    def update_user_is_active(email, is_active):
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise NotFound("User not found.")

        user.is_active = is_active
        user.save()
        return user

    @staticmethod
    def update_user(email, data):
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise NotFound("User not found with the provided email.")

        for key, value in data.items():
            if key == "password":
                setattr(user, "password", make_password(value))
            elif hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError(f"Invalid field '{key}' provided in data.")
        user.save()
        return user

    @staticmethod
    def bulk_update_users(data_list):
        updated_users = []
        failed = []

        for item in data_list:
            email = item.get("email")
            if not email:
                failed.append({"error": "Missing email", "data": item})
                continue

            try:
                user = User.objects.get(email=email)
                for key, value in item.items():
                    if key == "password":
                        setattr(user, "password", make_password(value))
                    elif hasattr(user, key):
                        setattr(user, key, value)
                    else:
                        raise ValueError(f"Invalid field '{key}' provided in data.")
                updated_users.append(user)
            except ObjectDoesNotExist:
                failed.append({"error": "User not found", "email": email})
            except Exception as e:
                failed.append({"error": str(e), "email": email})

        if updated_users:
            update_fields = [
                "email",
                "company_id",
                "authority",
                "password",
                "is_active",
            ]
            User.objects.bulk_update(updated_users, update_fields)

        return {
            "updated": len(updated_users),
            "failed": failed,
        }

    @staticmethod
    def verify_account(key):
        try:
            user = User.objects.get(key=key, is_verified=False)
        except ObjectDoesNotExist:
            raise NotFound("Invalid verification key or account already verified.")

        user.is_verified = True
        user.save()
        return True

    @staticmethod
    def get_user_profile(email):
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise NotFound("User not found.")

        return {
            "email": user.email,
            "company_id": user.company_id,
            "authority": user.authority,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }

    @staticmethod
    def deactivate_users_by_company(company_id):
        users = User.objects.filter(company_id=company_id, is_active=True)
        for user in users:
            user.is_active = False
            user.save()
        return users.count()

    @staticmethod
    def assign_authority_to_users(emails, authority):
        users = User.objects.filter(email__in=emails)
        for user in users:
            user.authority = authority
            user.save()
        return users.count()

    @staticmethod
    def delete_user(email):
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise NotFound("User not found.")
        user.delete()
        return True

    @staticmethod
    def delete_users_by_company(company_id):
        users = User.objects.filter(company_id=company_id)
        count = users.count()
        users.delete()
        return count
