from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.res_partner import ResPartner, ResPartnerData
from models.school_teacher import SchoolTeacherData
from models.school_holding import SchoolHolding
from models.school_school import SchoolSchool
from bson import ObjectId


class MainService(BaseService):

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        print(extra)
        holding_id = (
            ObjectId(extra.get("school_school").get("holding_id"))
            if extra.get("school_school").get("holding_id")
            else None
        )
        new_teacher_data = SchoolTeacherData(
            holding_id=holding_id,
            school_id=ObjectId(validated_data.get("school_id")),
            name=validated_data.get("name"),
            staff_no=validated_data.get("staff_no"),
            resident_no=validated_data.get("resident_no"),
            birth_date=validated_data.get("birth_date"),
            birth_place=validated_data.get("birth_place"),
            is_active=validated_data.get("is_active"),
        )
        SecurityValidator.validate_data(new_teacher_data)
        result = model.insert_one(new_teacher_data, user)
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }

    @staticmethod
    def list(
        model: BaseModel, query_params, params_validation, user, headers_dict=None
    ):
        result = model.aggregate(
            add_metadata=True,
            query_params=query_params,
            params_validation=params_validation,
            fields=query_params.get("fields"),
            exclude=query_params.get("exclude"),
            lookup=["school", "user"],
        )
        response_type = query_params.get("response_type")
        if response_type in ["xlsx"]:
            from helpers.openpyxl_helper import OpenpxlHelper

            export_data = [["No", "Nama", "NIP", "NIK", "username", "password"]]
            export_setting = [
                "w-5 text-center",
                "w-40",
                "w-25 center",
                "w-25 center",
                "w-20 center",
                "w-20 center",
            ]
            for idx, item in enumerate(result["data"], start=1):
                export_data.append(
                    [
                        idx,
                        item.get("name", ""),
                        item.get("staff_no", ""),
                        item.get("resident_no", ""),
                        (
                            item.get("user_info").get("login").split("_")[1]
                            if item.get("user_id")
                            else "-"
                        ),
                        (
                            item.get("user_info").get("password")
                            if item.get("user_id")
                            else "-"
                        ),
                    ]
                )

            export_kwargs = {
                "data": export_data,
                "setting": export_setting,
                "filename": "teacher",
                "title": "Data Guru",
            }

            helper_class = {
                "xlsx": OpenpxlHelper,
            }.get(response_type)

            return helper_class(**export_kwargs).response
        return result

    @staticmethod
    def account(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from models.res_user import ResUserData, ResUser
        from models.school_school import SchoolSchool
        from models.res_authority import ResAuthority
        from models.authentication_user import AuthenticationUserData
        from helpers.user_service import UserService

        from constants.access import Role

        if old_data.get("user_id"):
            raise ValidationError("Invalid teacher_id, account already exists")
        school_data = SchoolSchool().find_one(
            {"_id": ObjectId(old_data.get("school_id"))}
        )
        username = ResUser().get_school_username(
            old_data.get("school_id"),
            school_data.get("code"),
            old_data.get("name"),
        )
        authority_data = ResAuthority().find_one({"code": Role.TEACHER.value})
        new_user_data = ResUserData(
            holding_id=ObjectId(old_data.get("holding_id")),
            school_id=ObjectId(old_data.get("school_id")),
            teacher_id=ObjectId(_id),
            login=username,
            name=old_data.get("name"),
            authority_id=ObjectId(authority_data.get("_id")),
            authority_ids=[ObjectId(authority_data.get("_id"))],
            authority_codes=[authority_data.get("code")],
            is_password_encrypted=True,
            is_school=True,
            is_teacher=True,
            is_active=True,
        )
        new_auth_user_data = AuthenticationUserData(
            school_id=str(old_data.get("school_id")),
            holding_id=str(old_data.get("holding_id")),
            school_code=school_data.get("code"),
            username=new_user_data.login,
            password=new_user_data.password,
            role=",".join(new_user_data.authority_codes),
            is_staff=False,
            is_active=True,
            is_company_active=True,
        )
        SecurityValidator.validate_data(new_user_data, new_auth_user_data)
        ResUser().insert_one(new_user_data, user=user)
        UserService().create_user(new_auth_user_data)
        model.update_one(
            {"_id": ObjectId(_id)},
            {"user_id": new_user_data._id, "login": new_user_data.login},
        )
        return {
            "data": {"id": str(_id)},
            "message": None,
        }

    @staticmethod
    def input_xls(model: BaseModel, validated_data, extra, user, headers_dict=None):
        print(validated_data)
        print(extra)
        from utils.excel_util import ExcelUtils

        school_data = SchoolSchool().find_one(
            {"_id": ObjectId(validated_data.get("school_id"))}
        )
        holding_id = (
            ObjectId(school_data.get("holding_id"))
            if school_data.get("holding_id")
            else None
        )

        schema = {
            "NIP": {"type": "string", "required": False},
            "NIK": {"type": "string", "required": False},
            "NAMA": {"type": "string", "required": True},
        }

        excel_data = ExcelUtils.read(validated_data.get("file"), schema=schema)
        input_data = []
        for i in excel_data:
            new_teacher_data = SchoolTeacherData(
                holding_id=holding_id,
                school_id=ObjectId(validated_data.get("school_id")),
                name=i.get("NAMA"),
                staff_no=i.get("NIP"),
                resident_no=i.get("NIK"),
                is_active=True,
            )
            input_data.append(new_teacher_data)
        SecurityValidator.validate_data(input_data)
        if input_data:
            model.insert_many(input_data)
        return {
            "message": None,
        }
