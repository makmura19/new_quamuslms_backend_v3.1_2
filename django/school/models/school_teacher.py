from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from datetime import datetime

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class SchoolTeacherData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: Optional[ObjectId] = field(default=None)
    name: str
    user_id: Optional[ObjectId] = field(default=None)
    login: Optional[str] = field(default=None)
    staff_no: Optional[str] = field(default=None)
    resident_no: Optional[str] = field(default=None)
    birth_date: Optional[datetime] = field(default=None)
    birth_place: Optional[str] = field(default=None)
    is_active: bool


class SchoolTeacherSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=False, allow_none=True)
    name = ma_fields.String(required=True)
    user_id = ObjectIdField(required=False, allow_none=True)
    login = ma_fields.String(required=False, allow_none=True)
    staff_no = ma_fields.String(required=False, allow_none=True)
    resident_no = ma_fields.String(required=False, allow_none=True)
    birth_date = ma_fields.DateTime(required=False, allow_none=True)
    birth_place = ma_fields.String(required=False, allow_none=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class SchoolTeacher(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(SchoolTeacherData)
    collection_name = "school_teacher"
    schema = SchoolTeacherSchema
    search = ["name", "login", "staff_no", "resident_no"]
    object_class = SchoolTeacherData
    foreign_key = {
        "holding": {
            "local": "holding_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_holding"
            ).school_holding.SchoolHolding(),
        },
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "user": {
            "local": "user_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.res_user").res_user.ResUser(),
        },
    }

    def create_account(self, _id, secondary_role=None, user=None):
        """
            example:
                SchoolTeacher().create_account(coordinator_id, Role.TAHFIDZ_COORDINATOR, user)
                SchoolTeacher().create_account(coordinator_id, [Role.TAHFIDZ_TEACHER, TAHFIDZ_EXAMINER], user)
        """
        from rest_framework.exceptions import ValidationError
        from models.res_user import ResUserData, ResUser
        from models.school_school import SchoolSchool
        from models.res_authority import ResAuthority
        from models.authentication_user import AuthenticationUserData
        from helpers.user_service import UserService
        from helpers.security_validator import SecurityValidator
        from constants.access import Role, SCHOOL_ROLES

        teacher_data = self.find_one({"_id":ObjectId(_id)})
        if teacher_data.get("user_id"):
            raise ValidationError("Invalid teacher_id, account already exists.")
        
        school_id = ObjectId(teacher_data.get("school_id"))
        school_data = SchoolSchool().find_one(
            {"_id": school_id}
        )
        username = ResUser().get_school_username(
            school_id,
            school_data.get("code"),
            teacher_data.get("name"),
        )

        teacher_auth_data = ResAuthority().find_one({"code": Role.TEACHER.value})
        authority_id = ObjectId(teacher_auth_data.get("_id"))
        authority_ids = [authority_id]
        authority_codes = [Role.TEACHER.value]
        if secondary_role:
            if type(secondary_role) == list:
                for i in secondary_role:
                    if not i.value in SCHOOL_ROLES:
                        raise ValidationError(f"'{i.value}' does not exist in 'SCHOOL_ROLES'.")
                secondary_role = [i.value for i in secondary_role]
            else:
                if not secondary_role.value in SCHOOL_ROLES:
                    raise ValidationError(f"{secondary_role} does not exist in 'SCHOOL_ROLES'.")
                secondary_role = [secondary_role.value]
            secondary_auth_data = ResAuthority().find({"code": {"$in":secondary_role}})
            authority_ids += [ObjectId(i.get("_id")) for i in secondary_auth_data]
            authority_codes += secondary_role
        role = ",".join(authority_codes)

        new_user_data = ResUserData(
            holding_id=ObjectId(teacher_data.get("holding_id")) if teacher_data.get("holding_id") else None,
            school_id=school_id,
            teacher_id=ObjectId(_id),
            login=username,
            name=teacher_data.get("name"),
            authority_id=authority_id,
            authority_ids=authority_ids,
            authority_codes=authority_codes,
            is_teacher=True,
            is_active=True,
        )
        new_auth_user_data = AuthenticationUserData(
            school_id=str(school_id),
            holding_id=str(teacher_data.get("holding_id")) if teacher_data.get("holding_id") else "",
            school_code=school_data.get("code"),
            username=new_user_data.login,
            password=new_user_data.password,
            role=role,
            is_staff=False,
            is_active=True,
            is_company_active=True,
        )
        SecurityValidator.validate_data(new_user_data, new_auth_user_data)
        ResUser().insert_one(new_user_data, user=user)
        UserService().create_user(new_auth_user_data)
        self.update_one(
            {"_id": ObjectId(_id)},
            {"user_id": new_user_data._id, "login": new_user_data.login},
            user=user
        )


    def pull_secondary_role(self, _id, role, user=None):
        """
            example:
                SchoolTeacher().pull_secondary_role(coordinator_id, Role.TAHFIDZ_COORDINATOR, user)
                SchoolTeacher().pull_secondary_role(coordinator_id, user, [Role.TAHFIDZ_TEACHER, TAHFIDZ_EXAMINER])
        """
        from rest_framework.exceptions import ValidationError
        from models.res_user import ResUser
        from models.res_authority import ResAuthority
        from helpers.user_service import UserService
        from constants.access import Role, SCHOOL_ROLES

        teacher_data = self.find_one({"_id":ObjectId(_id)})
        if not teacher_data.get("user_id"):
            raise ValidationError("Invalid teacher_id, account not exists yet.")
        
        user_data = ResUser().find_one({"_id":ObjectId(teacher_data.get("user_id"))})
        if role.value == Role.TEACHER.value:
            raise ValidationError("Invalid role.")
        if type(role) == list:
            for i in role:
                if not i.value in SCHOOL_ROLES:
                    raise ValidationError(f"'{i.value}' does not exist in 'SCHOOL_ROLES'.")
                if not i.value in user_data.get("authority_codes"):
                    raise ValidationError(f"Teacher user does not have role '{i.value}'.")
            role = [i.value for i in role]
        else:
            if not role.value in SCHOOL_ROLES:
                raise ValidationError(f"{role} does not exist in 'SCHOOL_ROLES'.")
            if not role.value in user_data.get("authority_codes"):
                raise ValidationError(f"Teacher user does not have role '{role.value}'.")
            role = [role.value]

        auth_data = ResAuthority().find({"code":{"$in":role}})
        auth_ids = [ObjectId(i.get("_id")) for i in auth_data]
        ResUser().update_one(
            {"_id":ObjectId(teacher_data.get("user_id"))},
            pull_data={
                "authority_ids":auth_ids,
                "authority_codes":role
            },
            user=user
        )
        new_user_data = ResUser().find_one({"_id":ObjectId(teacher_data.get("user_id"))})
        UserService().assign_authority_to_users(
            [new_user_data.get("login")], 
            ",".join(new_user_data.get("authority_codes"))
        )


    def add_secondary_role(self, _id, role, user=None):
        """
            example:
                SchoolTeacher().add_secondary_role(coordinator_id, Role.TAHFIDZ_COORDINATOR, user)
                SchoolTeacher().add_secondary_role(coordinator_id, user, [Role.TAHFIDZ_TEACHER, TAHFIDZ_EXAMINER])
        """
        from rest_framework.exceptions import ValidationError
        from models.res_user import ResUser
        from models.res_authority import ResAuthority
        from helpers.user_service import UserService
        from constants.access import Role, SCHOOL_ROLES

        teacher_data = self.find_one({"_id":ObjectId(_id)})
        if not teacher_data.get("user_id"):
            raise ValidationError("Invalid teacher_id, account not exists yet.")
        
        user_data = ResUser().find_one({"_id":ObjectId(teacher_data.get("user_id"))})
        if role.value == Role.TEACHER.value:
            raise ValidationError("Invalid role.")
        if type(role) == list:
            for i in role:
                if not i.value in SCHOOL_ROLES:
                    raise ValidationError(f"'{i.value}' does not exist in 'SCHOOL_ROLES'.")
                if i.value in user_data.get("authority_codes"):
                    raise ValidationError(f"Teacher already have role '{i.value}'.")
            role = [i.value for i in role]
        else:
            if not role.value in SCHOOL_ROLES:
                raise ValidationError(f"{role} does not exist in 'SCHOOL_ROLES'.")
            if role.value in user_data.get("authority_codes"):
                raise ValidationError(f"Teacher already have role '{role.value}'.")
            role = [role.value]

        auth_data = ResAuthority().find({"code":{"$in":role}})
        auth_ids = [ObjectId(i.get("_id")) for i in auth_data]
        ResUser().update_one(
            {"_id":ObjectId(teacher_data.get("user_id"))},
            add_to_set_data={
                "authority_ids":auth_ids,
                "authority_codes":role
            },
            user=user
        )
        new_user_data = ResUser().find_one({"_id":ObjectId(teacher_data.get("user_id"))})
        UserService().assign_authority_to_users(
            [new_user_data.get("login")], 
            ",".join(new_user_data.get("authority_codes"))
        )