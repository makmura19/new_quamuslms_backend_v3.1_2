from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from constants.params_validation_type import ParamsValidationType
from models.edu_subject import EduSubject
from helpers.custom_serializer_field import FileField, FILETYPEGROUP


class CreateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    short_name = serializers.CharField(required=True)
    color = serializers.CharField(required=False, allow_blank=True)
    is_catalogue = serializers.BooleanField(required=True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {}
        

class SequenceSerializer(BaseSerializer):
    _ids = serializers.ListField(child=serializers.CharField(), required=True)
    
    class Meta:
        validate_model = {
            "_id": {
                "field": "_id",
                "model": EduSubject(),
                "type": ParamsValidationType.OBJECT_IDS
            }
        }
        
        
class UploadImagesSerializer(BaseSerializer):
    file1 = FileField(
        required=False, allowed_types=[*FILETYPEGROUP.IMAGE], max_size_mb=15
    )
    file2 = FileField(
        required=False, allowed_types=[*FILETYPEGROUP.IMAGE], max_size_mb=15
    )

    class Meta:
        validate_model = {}
