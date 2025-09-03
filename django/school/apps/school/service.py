from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.res_partner import ResPartner, ResPartnerData
from models.school_holding import SchoolHolding
from models.school_school import SchoolSchoolData, SchoolSchool
from bson import ObjectId


class MainService(BaseService):

    @staticmethod
    def create(model: SchoolSchool, validated_data, extra, user, headers_dict=None):
        from models.edu_stage_group import EduStageGroup

        stage_data = extra.get("edu_stage")
        group_data = EduStageGroup().find_one(
            {"_id": ObjectId(stage_data.get("group_id"))}
        )
        new_partner_data = ResPartnerData(
            name=validated_data.get("name"),
            address=validated_data.get("address"),
            is_school=True,
        )
        code = validated_data.get("code")
        if not code:
            code = model.get_code()
        new_school_data = SchoolSchoolData(
            stage_id=ObjectId(validated_data.get("stage_id")),
            stage_group_id=ObjectId(stage_data.get("group_id")),
            stage_group_level=group_data.get("sequence"),
            partner_id=new_partner_data._id,
            code=code,
            name=validated_data.get("name"),
            npsn=validated_data.get("npsn"),
            group_ids=validated_data.get("group_ids"),
            tz=validated_data.get("tz"),
        )
        SecurityValidator.validate_data(new_partner_data, new_school_data)
        ResPartner().insert_one(new_partner_data, user)
        result = model.insert_one(new_school_data, user)
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }

    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        update_partner_data = {
            "name": validated_data.get("name"),
            "address": validated_data.get("address"),
        }
        validated_data.pop("address")
        update_school_data = {**validated_data}
        ResPartner().update_one(
            {"_id": ObjectId(old_data.get("partner_id"))},
            update_data=update_partner_data,
            user=user,
        )
        model.update_one(
            {"_id": ObjectId(_id)}, update_data=update_school_data, user=user
        )
        if (
            old_data.get("holding_id") is None
            and validated_data.get("holding_id") is not None
        ):
            SchoolHolding().update_one(
                {"_id": ObjectId(validated_data.get("holding_id"))},
                add_to_set_data={"school_ids": [ObjectId(_id)]},
                user=user,
            )
        elif (
            old_data.get("holding_id") is not None
            and validated_data.get("holding_id") is None
        ):
            SchoolHolding().update_one(
                {"_id": ObjectId(old_data.get("holding_id"))},
                pull_data={"school_ids": [ObjectId(_id)]},
                user=user,
            )
        return {
            "data": {"id": str(_id)},
            "message": None,
        }

    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        ResPartner().soft_delete(
            {"_id": ObjectId(old_data.get("partner_id"))}, old_data, user=user
        )
        model.soft_delete({"_id": ObjectId(_id)}, old_data, user=user)
        if old_data.get("holding_id") is not None:
            SchoolHolding().update_one(
                {"_id": ObjectId(old_data.get("holding_id"))},
                pull_data={"school_ids": [ObjectId(_id)]},
                user=user,
            )
        return {}

    @staticmethod
    def list(
        model: BaseModel, query_params, params_validation, user, headers_dict=None
    ):
        from constants.aggregation import FieldType
        from constants.access import Role, SCHOOL_ROLES, HOLDING_ROLES, STAFF_ROLES

        query = {}

        if any(role in user.role.split(",") for role in HOLDING_ROLES):
            from models.school_holding import SchoolHolding

            holding_data = SchoolHolding().find_one({"_id": ObjectId(user.holding_id)})
            query["_id"] = {
                "$in": [ObjectId(item) for item in holding_data.get("school_ids")]
            }
        elif any(role in user.role.split(",") for role in SCHOOL_ROLES):
            query["_id"] = {"$in": [ObjectId(user.school_id)]}

        result = model.aggregate(
            add_metadata=True,
            query=query,
            query_params=query_params,
            params_validation=params_validation,
            fields=query_params.get("fields"),
            exclude=query_params.get("exclude"),
            lookup=["partner"],
            additional_fields={
                "complete_address": {
                    "type": FieldType.CONCAT,
                    "value": [
                        "$partner_info.address.street",
                        " Ds. ",
                        "$partner_info.address.village",
                        " Kec. ",
                        "$partner_info.address.district",
                        " ",
                        "$partner_info.address.city",
                        " ",
                        "$partner_info.address.province",
                        ", ",
                        "$partner_info.address.zipcode",
                    ],
                }
            },
        )
        return result

    @staticmethod
    def retrieve(
        model: BaseModel,
        _id,
        user,
        headers_dict=None,
        query_params={},
        params_validation={},
    ):
        from constants.params_validation_type import ParamsValidationType

        result = model.aggregate(
            query_params={**query_params, "_id": ObjectId(_id)},
            params_validation={
                **params_validation,
                "_id": ParamsValidationType.OBJECT_ID,
            },
            lookup=["partner"],
        )
        return result[0]

    @staticmethod
    def level(
        model: BaseModel,
        _id,
        user,
        headers_dict=None,
        query_params={},
        params_validation={},
    ):
        from models.edu_stage_group import EduStageGroup
        from models.edu_stage_level import EduStageLevel
        from models.school_school import SchoolSchool

        school_data = SchoolSchool().find_one({"_id": ObjectId(_id)})
        stage_group_data = EduStageGroup().find_one(
            {"_id": ObjectId(school_data.get("stage_group_id"))}
        )
        level_ids = [ObjectId(item) for item in stage_group_data.get("level_ids")]
        level_data = EduStageLevel().find({"_id": {"$in": level_ids}})
        return level_data

    @staticmethod
    def activate(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from models.res_user import ResUser, ResUserData
        from models.school_staff import SchoolStaff, SchoolStaffData
        from models.authentication_user import AuthenticationUserData
        from helpers.user_service import UserService
        from utils.string_util import StringUtil
        from models.res_authority import ResAuthority
        from constants.access import Role

        if old_data.get("is_active") == validated_data.get("is_active"):
            raise ValidationError("Invalid school_id")

        model.update_one(
            {"_id": ObjectId(_id)},
            {"is_active": validated_data.get("is_active"), "is_client": True},
        )
        if validated_data.get("is_active"):
            username = f"{old_data.get('code')}_admin"
            admin_user_data = ResUser().find_one({"login": username})
            if not admin_user_data:
                authority_data = ResAuthority().find_one(
                    {"code": Role.ADMINISTRATOR.value}
                )
                new_user_data = ResUserData(
                    school_id=ObjectId(_id),
                    login=f"{old_data.get('code')}_admin",
                    password=StringUtil.generate_code("nnnnn"),
                    name="Administrator",
                    authority_id=ObjectId(authority_data.get("_id")),
                    authority_ids=[ObjectId(authority_data.get("_id"))],
                    authority_codes=[authority_data.get("code")],
                    is_admin=True,
                    is_password_encrypted=False,
                    is_school=True,
                    is_active=True,
                )
                new_staff_data = SchoolStaffData(
                    school_id=ObjectId(_id),
                    name=new_user_data.name,
                    role_id=new_user_data.authority_id,
                    login=new_user_data.login,
                    user_id=new_user_data._id,
                )
                new_auth_user_data = AuthenticationUserData(
                    school_id=_id,
                    school_code=old_data.get("code"),
                    username=new_user_data.login,
                    password=new_user_data.password,
                    role=",".join(new_user_data.authority_codes),
                    is_staff=False,
                    is_active=True,
                    is_company_active=True,
                )
                SecurityValidator.validate_data(
                    new_user_data, new_staff_data, new_auth_user_data
                )
                UserService.create_user(new_auth_user_data)
                ResUser().insert_one(new_user_data, user=user)
                SchoolStaff().insert_one(new_staff_data, user=user)
                model.update_one(
                    {"_id": ObjectId(_id)},
                    add_to_set_data={"staff_ids": [new_staff_data._id]},
                )
        return {
            "data": {"id": str(_id)},
            "message": None,
        }

    @staticmethod
    def teacher_account(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from models.school_teacher import SchoolTeacher
        from models.res_user import ResUser, ResUserData
        from models.authentication_user import AuthenticationUserData
        from models.res_authority import ResAuthority
        from constants.access import Role
        from helpers.user_service import UserService

        teacher_data = SchoolTeacher().find(
            {"school_id": ObjectId(_id), "user_id": None}
        )
        authority_data = ResAuthority().find_one({"code": Role.TEACHER.value})
        input_user_data = []
        input_auth_user_data = []
        update_teacher_data = []
        for i in teacher_data:
            username = ResUser().get_school_username(
                _id,
                old_data.get("code"),
                i.get("name"),
            )
            new_user_data = ResUserData(
                holding_id=ObjectId(old_data.get("holding_id")),
                school_id=ObjectId(old_data.get("school_id")),
                teacher_id=ObjectId(_id),
                login=username,
                name=i.get("name"),
                authority_id=ObjectId(authority_data.get("_id")),
                authority_ids=[ObjectId(authority_data.get("_id"))],
                authority_codes=[authority_data.get("code")],
                is_password_encrypted=True,
                is_school=True,
                is_teacher=True,
                is_active=True,
            )
            new_auth_user_data = AuthenticationUserData(
                school_id=_id,
                holding_id=str(old_data.get("holding_id")),
                school_code=old_data.get("code"),
                username=new_user_data.login,
                password=new_user_data.password,
                role=",".join(new_user_data.authority_codes),
                is_staff=False,
                is_active=True,
                is_company_active=True,
            )
            input_user_data.append(new_user_data)
            input_auth_user_data.append(new_auth_user_data)
            update_teacher_data.append(
                {
                    "_id": i.get("_id"),
                    "set_data": {"user_id": new_user_data._id, "login": username},
                }
            )
        SecurityValidator.validate_data(input_user_data, input_auth_user_data)
        if input_user_data:
            ResUser().insert_many(input_user_data)
        if input_auth_user_data:
            UserService().bulk_create_users(input_auth_user_data)
        if update_teacher_data:
            SchoolTeacher().update_many_different_data(update_teacher_data)
        return {
            "data": {"id": str(_id)},
            "message": None,
        }

    @staticmethod
    def upload_logo(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from utils.file_storage_util import FileStorageUtil

        url = FileStorageUtil.upload_aws(validated_data.get("file"), "school_logo")
        if not url:
            raise ValidationError("Upload logo gagal.")
        update_data = {"logo_md": url[0]}
        model.update_one({"_id": ObjectId(_id)}, update_data, user=user)
        return {
            "data": {"id": str(_id)},
            "message": None,
        }

    @staticmethod
    def module(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from .module import Module
        from rest_framework.exceptions import ValidationError

        if not old_data.get("is_active"):
            raise ValidationError("Invalid _id, school is inactive")

        Module(_id, old_data, validated_data, extra, user)

        return {
            "data": {"id": str(_id)},
            "message": None,
        }
