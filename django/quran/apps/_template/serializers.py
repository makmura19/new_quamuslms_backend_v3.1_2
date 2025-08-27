from helpers.base_serializer import BaseSerializer
from rest_framework import serializers

from models.demo_author import DemoAuthor
from models.demo_publisher import DemoPublisher
from models.demo_book_category import DemoBookCategory
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    author_ids = serializers.ListField(child=serializers.CharField(), allow_empty=False)
    publisher_id = serializers.CharField(required=True, max_length=255)
    category_ids = serializers.ListField(
        child=serializers.CharField(), allow_empty=False
    )
    name = serializers.CharField(required=True, max_length=255)
    isbn = serializers.CharField(required=True, max_length=255)
    published_at = serializers.DateField()
    description = serializers.CharField(required=True)
    price = serializers.IntegerField()
    stock_quantity = serializers.IntegerField()

    class Meta:
        validate_model = {
            "author_ids": {
                "field": "_id",
                "model": DemoAuthor(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "publisher_id": {
                "field": "_id",
                "model": DemoPublisher(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "category_ids": {
                "field": "_id",
                "model": DemoBookCategory(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }
