from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.edu_subject import EduSubject
from models.edu_stage_level import EduStageLevel
from constants.params_validation_type import ParamsValidationType
from helpers.custom_serializer_field import FileField, FILETYPEGROUP


class CreateSerializer(BaseSerializer):
    subject_id = serializers.CharField(required=True)
    level_id = serializers.CharField(required=True)

    class Meta:
        validate_model = {
            "subject_id": {
                "field": "_id",
                "model": EduSubject(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "level_id": {
                "field": "_id",
                "model": EduStageLevel(),
                "type": ParamsValidationType.OBJECT_ID,
            },
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
