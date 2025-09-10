from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from utils.file_storage_util import FileStorageUtil


class MainService(BaseService):

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        url = FileStorageUtil.upload_aws(validated_data.get("file"), "tiptap_rte")
        if len(url) > 0:
            return {"src": url[0]}

        return {
            "data": {},
            "message": None,
        }
