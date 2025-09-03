from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.quran_report_type import QuranReportTypeData
from bson import ObjectId


class MainService(BaseService):

    @staticmethod
    def upload_preview(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from utils.file_storage_util import FileStorageUtil

        url = FileStorageUtil.upload_aws(validated_data.get("file"), "quran_preview")
        if not url:
            raise ValidationError("Failed to upload image.")
        update_data = {"preview": url[0]}
        model.update_one({"_id": ObjectId(_id)}, update_data, user=user)
        return {
            "data": {"id": str(_id)},
            "message": None,
        }
