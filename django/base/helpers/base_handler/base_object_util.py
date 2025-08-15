from bson import ObjectId
from rest_framework.exceptions import NotFound
from utils.id_util import IDUtil
from constants.access import Role
import os


class BaseObjectUtil:
    @staticmethod
    def get_object(model, data_name, pk=None, convert_to_json=True, user=None):
        # company_id = os.environ.get("COMPANY_ID")
        query = {"_id": ObjectId(pk)}

        # if user and not getattr(user, "is_staff", False):
        #     value = getattr(user, company_id, None)
        #     if value:
        #         query[company_id] = ObjectId(value)

        result = model.find_one(
            query,
            convert_to_json=convert_to_json,
        )
        if not result:
            raise NotFound(detail=f"{data_name} tidak ditemukan")
        return result
