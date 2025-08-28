from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.finance_merchant import FinanceMerchant, FinanceMerchantData
from models.config_finance import ConfigFinance
from bson import ObjectId

class MainService(BaseService):
    
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        import copy
        
        filtering = None
        if value.get("holding_id"):
            filtering = {"holding_id":ObjectId(value.get("holding_id"))}
        if value.get("school_id"):
            filtering = {"school_id":ObjectId(value.get("school_id"))}
        value.update({"filter":copy.deepcopy(filtering)})
        filtering.update({"name":value.get("name")})

        if value.get("holding_id") and value.get("school_id"):
            raise ValidationError(f"holding_id and school_id cannot be filled in both.")
        if not value.get("holding_id") and not value.get("school_id"):
            raise ValidationError(f"One of holding_id and school_id must be filled.")
        
        existing_data = FinanceMerchant().find_one(filtering)
        if existing_data:
            raise ValidationError(f"The name '{value.get('name')}' already exists.")

        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        new_merchant_data = FinanceMerchantData(
            holding_id=validated_data.get("holding_id"),
            school_id=validated_data.get("school_id"),
            name=validated_data.get("name"),
            phone=validated_data.get("phone"),
            is_school=True if validated_data.get("school_id") else False,
            is_holding=True if validated_data.get("holding_id") else False,
        )
        SecurityValidator.validate_data(new_merchant_data)
        result = model.insert_one(new_merchant_data, user)
        # ----- belum ada data config_finance
        # ConfigFinance().update_one(
        #     validated_data.get(filter),
        #     add_to_set_data={"merchant_ids":[new_merchant_data._id]}
        # )
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }

    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        filtering = {"_id":{"$ne":old_data.get("_id")}}
        if old_data.get("holding_id"):
            filtering.update({"holding_id":ObjectId(old_data.get("holding_id"))})
        if old_data.get("school_id"):
            filtering.update({"school_id":ObjectId(old_data.get("school_id"))})
        existing_data = FinanceMerchant().find(filtering)
        existing_name = [i.get("name") for i in existing_data]
        if value.get("name") in existing_name:
            raise ValidationError(f"The name '{value.get('name')}' already exists.")

        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}


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
            lookup=["holding","school","user","coa"]
        )
        return result


    @staticmethod
    def account(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from models.res_user import ResUserData, ResUser
        from models.school_holding import SchoolHolding
        from models.school_school import SchoolSchool
        from models.res_authority import ResAuthority
        from models.authentication_user import AuthenticationUserData
        from helpers.user_service import UserService

        from constants.access import Role

        if old_data.get("user_id"):
            raise ValidationError("Invalid merchant_id, account already exists")
        
        holding_id = ObjectId(old_data.get("holding_id")) if old_data.get("holding_id") else None
        school_id = ObjectId(old_data.get("school_id")) if old_data.get("school_id") else None
        username = ""
        school_data = None
        school_code = ""
        if holding_id:
            holding_data = SchoolHolding().find_one({"_id": holding_id})
            username = ResUser().get_holding_username(
                _id=holding_id, 
                code=holding_data.get("code"), 
                name=old_data.get("name")
            )
            school_code = holding_data.get("code")
        else:
            school_data = SchoolSchool().find_one({"_id": school_id})
            username = ResUser().get_school_username(
                _id=school_id,
                code=school_data.get("code"),
                name=old_data.get("name"),
            )
            school_code = school_data.get("code")
        
        authority_data = ResAuthority().find_one({"code": Role.MERCHANT.value})
        new_user_data = ResUserData(
            holding_id=holding_id,
            school_id=school_id,
            merchant_id=ObjectId(_id),
            login=username,
            name=old_data.get("name"),
            authority_id=ObjectId(authority_data.get("_id")),
            authority_ids=[ObjectId(authority_data.get("_id"))],
            authority_codes=[authority_data.get("code")],
            is_password_encrypted=False,
            is_merchant=True,
            is_active=True,
        )
        
        new_auth_user_data = AuthenticationUserData(
            school_id=str(school_id) if school_id else "",
            holding_id=str(holding_id) if holding_id else "",
            school_code=school_code,
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
