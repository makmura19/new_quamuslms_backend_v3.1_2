from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.res_partner import ResPartner, ResPartnerData
from models.school_school import SchoolSchool
from models.school_holding import SchoolHoldingData, SchoolHolding
from bson import ObjectId


class MainService(BaseService):
    @staticmethod
    def create(model: SchoolHolding, validated_data, extra, user, headers_dict=None):
        school_ids = [ObjectId(item) for item in validated_data.get("school_ids")]
        code = validated_data.get("code")
        if not code:
            code = model.get_code()
        new_partner_data = ResPartnerData(
            name=validated_data.get("name"),
            address=validated_data.get("address"),
            is_holding=True,
        )
        new_holding_data = SchoolHoldingData(
            code=code,
            partner_id=new_partner_data._id,
            name=validated_data.get("name"),
            is_active=validated_data.get("is_active"),
            school_ids=school_ids,
        )

        SecurityValidator.validate_data(new_partner_data, new_holding_data)
        ResPartner().insert_one(new_partner_data, user)
        result = model.insert_one(new_holding_data, user)
        if school_ids:
            SchoolSchool().update_many(
                {"_id": {"$in": school_ids}},
                {"holding_id": new_holding_data._id, "under_holding": True},
            )
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }

    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        school_ids = [ObjectId(item) for item in validated_data.get("school_ids")]
        update_partner_data = {
            "name": validated_data.get("name"),
            "address": validated_data.get("address"),
        }
        update_holding_data = {
            "name": validated_data.get("name"),
            "is_active": validated_data.get("is_active"),
        }
        ResPartner().update_one(
            {"_id": ObjectId(old_data.get("partner_id"))},
            update_data=update_partner_data,
            user=user,
        )
        model.update_one(
            {"_id": ObjectId(_id)}, update_data=update_holding_data, user=user
        )
        if old_data.get("school_ids"):
            SchoolSchool().update_many(
                {"_id": {"$in": old_data.get("school_ids")}},
                {"holding_id": None, "under_holding": False},
            )
        if school_ids:
            SchoolSchool().update_many(
                {"_id": {"$in": school_ids}},
                {"holding_id": ObjectId(_id), "under_holding": True},
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
        return {}

    @staticmethod
    def list(
        model: BaseModel, query_params, params_validation, user, headers_dict=None
    ):
        from constants.aggregation import FieldType

        result = model.aggregate(
            add_metadata=True,
            query_params=query_params,
            params_validation=params_validation,
            fields=query_params.get("fields"),
            exclude=query_params.get("exclude"),
            lookup=["partner", "staffs", "schools"],
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
    def upload_logo(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from utils.file_storage_util import FileStorageUtil
        from helpers.user_service import UserService

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
    def staff(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        print(validated_data)
        print(extra)
        from models.res_user import ResUser, ResUserData
        from models.authentication_user import AuthenticationUserData
        from models.school_staff import SchoolStaff, SchoolStaffData
        from utils.string_util import StringUtil
        from helpers.user_service import UserService

        username = ResUser().get_holding_username(
            _id=_id, code=old_data.get("code"), name=validated_data.get("name")
        )
        new_user_data = ResUserData(
            holding_id=ObjectId(_id),
            login=username,
            password=StringUtil.generate_code("nnnnn"),
            name=validated_data.get("name"),
            authority_id=ObjectId(validated_data.get("role_id")),
            authority_ids=[ObjectId(validated_data.get("role_id"))],
            authority_codes=[extra.get("res_authority").get("code")],
            is_password_encrypted=False,
            is_holding=True,
            is_active=True,
        )

        new_auth_user_data = AuthenticationUserData(
            holding_id=_id,
            school_code=old_data.get("code"),
            username=new_user_data.login,
            password=new_user_data.password,
            role=",".join(new_user_data.authority_codes),
            is_staff=False,
            is_active=True,
            is_company_active=True,
        )
        new_school_staff_data = SchoolStaffData(
            holding_id=ObjectId(_id),
            name=validated_data.get("name"),
            role_id=ObjectId(validated_data.get("role_id")),
            login=username,
            user_id=new_user_data._id,
        )
        SecurityValidator.validate_data(
            new_user_data, new_auth_user_data, new_school_staff_data
        )
        ResUser().insert_one(new_user_data, user=user)
        UserService().create_user(new_auth_user_data)
        SchoolStaff().insert_one(new_school_staff_data)
        model.update_one(
            {"_id": ObjectId(_id)},
            add_to_set_data={"staff_ids": [new_school_staff_data._id]},
        )

        return {
            "data": {"id": str(_id)},
            "message": None,
        }
