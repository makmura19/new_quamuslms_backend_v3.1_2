import json
import uuid

from marshmallow.validate import OneOf
from marshmallow import ValidationError, fields
from helpers.mongodb_connection import MongoDBConnection
from datetime import datetime, timezone
from utils.mongo_json_encoder import MongoJSONEncoder
from utils.dict_util import DictUtil
from constants.aggregation import UpdateOperator, FieldType
from helpers.query_builder import build_find_query
from helpers.custom_model_field import ObjectIdField, ObjectIdsField
import logging
from pymongo import UpdateOne
from bson.objectid import ObjectId
from constants.params_validation_type import ParamsValidationType
from constants.relation import RelationType
from dataclasses import asdict, is_dataclass, fields as dc_fields
import inspect
from utils.logging_util import LoggingUtil
from copy import deepcopy
from helpers.field_type_handlers.registry import registry

audit_logger = logging.getLogger("audit")

"""
additional_fields={
    "complete_address": {
        "type": CONCAT,
        "value": ["$address.street", " Ds. ", "$address.village"],
    }
}
group={
    "_id": {
        "grade_id": "$grade_id",
        "grade_name": "$demo_author_grade_info.name",
    },
    "aggregation": {"$salary": [[GROUP_AVG, 0], [GROUP_SUM, 0]]},
}
"""


"""
BaseModel

Custom ORM berbasis PyMongo + Marshmallow untuk digunakan di proyek Django.

Fitur utama:
- Validasi schema dengan marshmallow
- Insert, update, soft delete
- Query builder dinamis (filter, sort, pagination, search)
- Aggregation builder + addFields + group
- Lookup relasi seperti ORM
- Dukungan metadata, timestamp, is_deleted, dan nested projection

Contoh subclass:
    class BookModel(BaseModel):
        collection_name = "books"
        schema = BookSchema
        search = ["title", "author"]
        foreign_key = {
            "author_id": {"model": AuthorModel(), "key": "_id"},
        }
        indexed_fields = ["title", "author_id"]
"""

SENSITIVE_KEYS = {"password", "token", "secret", "api_key", "access_token"}
IMMUTABLE_FIELDS = {"_id", "created_at"}


class BaseModel:
    collection_name = None
    schema = None
    search = []
    foreign_key = []
    timezone = "UTC"

    def __init__(self):
        self.db = MongoDBConnection().get_database()
        if not self.collection_name:
            raise ValueError("collection_name harus ditentukan di subclass.")

    def filter_dataclass_fields(self, cls, data: dict):
        valid_fields = {f.name for f in dc_fields(cls)}
        return {k: v for k, v in data.items() if k in valid_fields}

    def mask_sensitive_data(self, data):
        masked = {}
        if not data:
            return None
        for k, v in data.items():
            if k.lower() in SENSITIVE_KEYS:
                masked[k] = "***MASKED***"
            else:
                masked[k] = v
        return masked

    def remove_immutable_fields(self, data):
        return {k: v for k, v in data.items() if k not in IMMUTABLE_FIELDS}

    def strip_undeclared_fields(self, dataclass_instance, source_keys):
        result = {}
        for f in dc_fields(dataclass_instance):
            if f.name in source_keys:
                result[f.name] = getattr(dataclass_instance, f.name)
        return result

    def new(self, **kwargs):
        clean_kwargs = self.filter_dataclass_fields(self.object_class, kwargs)
        return self.object_class(**clean_kwargs)

    def update_sequence(self, data, key="sequence"):
        from utils.array_util import ArrayUtil

        if not ArrayUtil.is_unique(data):
            raise ValidationError("Sequence_ids tidak valid.")

        data = [
            {"_id": ObjectId(i), "set_data": {key: idx}}
            for idx, i in enumerate(data, start=1)
        ]
        self.update_many_different_data(data)

    def prepare_common_fields(self, data: dict, is_new=False) -> dict:
        now = datetime.now(timezone.utc)
        data["updated_at"] = now
        if is_new:
            data.setdefault("created_at", now)
            data.setdefault("is_deleted", False)
        return data

    def parse_object_id(self, _id):
        if hasattr(self, "type_id"):
            if self.type_id == ParamsValidationType.OBJECT_ID:
                return ObjectId(_id)
            elif self.type_id == ParamsValidationType.INT:
                return int(_id)
        return str(_id)

    def validated_and_clean_data(self, data, partial=False):
        if is_dataclass(data):
            data = asdict(data)
        validated = self.validate_data(data, partial=partial)
        return validated

    def set_timezone(self, tz="UTC"):
        self.timezone = tz

    def get_id(self, pk):
        if self.type_id == ParamsValidationType.OBJECT_ID:
            _id = f"oid{pk}"
        elif self.type_id == ParamsValidationType.STRING:
            _id = str(pk)
        elif self.type_id == ParamsValidationType.INT:
            _id = int(pk)
        return _id

    @property
    def collection(self):
        return self.db[self.collection_name]

    def filter_dataclass_fields(self, cls, data: dict):
        valid_fields = {f.name for f in inspect.signature(cls).parameters.values()}
        return {k: v for k, v in data.items() if k in valid_fields}

    def validate_data(self, data, partial=False):
        from dataclasses import is_dataclass, asdict
        from marshmallow.exceptions import ValidationError

        try:
            if is_dataclass(data):
                data = asdict(data)
            schema_instance = self.schema(partial=partial)
            schema_fields = set(schema_instance.fields.keys())
            filtered_data = {k: v for k, v in data.items() if k in schema_fields}
            validated = schema_instance.load(filtered_data)
            return validated

        except ValidationError as e:
            raise ValueError(f"Data tidak valid: {e.messages}")

    def _prepare_data_for_insert(self, data):
        prepared_data = {
            **data,
            "is_deleted": data.get("is_deleted", False),
            "created_at": data.get("created_at", datetime.now(timezone.utc)),
            "updated_at": data.get("updated_at", datetime.now(timezone.utc)),
        }
        return prepared_data

    def count_data(self, query={}, include_deleted=False):
        if not include_deleted:
            query["is_deleted"] = False
        return self.collection.count_documents(query)

    def aggregate_field(
        self,
        field_name,
        query=None,
        include_deleted=False,
        agg_type="sum",  # "sum", "avg", "max", "min"
    ):
        """
        Contoh:
            aggregate_field("debit", query={"school_id": "abc"}, agg_type="sum")
            aggregate_field("debit", agg_type="avg")
        """

        if query is None:
            query = {}

        query = dict(query)

        if not include_deleted:
            query.setdefault("is_deleted", False)

        agg_map = {
            "sum": "$sum",
            "avg": "$avg",
            "max": "$max",
            "min": "$min",
        }

        if agg_type not in agg_map:
            raise ValueError(f"Unsupported aggregation type: {agg_type}")

        pipeline = [
            {"$match": query},
            {"$group": {"_id": None, "result": {agg_map[agg_type]: f"${field_name}"}}},
        ]

        result = list(self.collection.aggregate(pipeline))
        return result[0]["result"] if result else 0

    def get_user_log(self, user=None):
        user_info = " "
        if user:
            value = getattr(user, user.USERNAME_FIELD)
            user_info = f" user={value} "
        return user_info

    def insert_one(self, data, user=None):
        validated_data = self.validated_and_clean_data(data)
        validated_data = self.prepare_common_fields(validated_data, is_new=True)
        inserted_data = self.collection.insert_one(validated_data)
        # if user:
        #     from models.ir_audit_log import IrAuditLog

        #     IrAuditLog().create_log(
        #         self, user, "create", inserted_data.inserted_id, validated_data
        #     )
        return inserted_data

    def insert_many(self, data_list):
        validated_data_list = [
            self.prepare_common_fields(
                self.validated_and_clean_data(asdict(data)), is_new=True
            )
            for data in data_list
        ]
        result = self.collection.insert_many(validated_data_list)
        result = [str(id) for id in result.inserted_ids]
        return result

    def update_one(
        self,
        query,
        update_data=None,
        inc_data=None,
        dec_data=None,
        add_to_set_data=None,
        pull_data=None,
        user=None,
    ):
        query_data = {}

        if update_data:
            if any("." in k for k in update_data.keys()):
                validated_data = deepcopy(update_data)
            else:
                validated_data = self.validated_and_clean_data(
                    update_data, partial=True
                )
            validated_data = self.prepare_common_fields(validated_data, is_new=False)
        else:
            validated_data = {"updated_at": datetime.now(timezone.utc)}

        validated_data = self.remove_immutable_fields(validated_data)
        query_data[UpdateOperator.SET] = validated_data

        combined_inc = {}
        if inc_data:
            combined_inc.update(inc_data)
        if dec_data:
            dec_data = {k: -v for k, v in dec_data.items()}
            combined_inc.update(dec_data)
        if combined_inc:
            query_data[UpdateOperator.INC] = combined_inc

        if add_to_set_data:
            query_data[UpdateOperator.ADD_TO_SET] = {}
            for k, v in add_to_set_data.items():
                if not isinstance(v, list):
                    v = [v]
                query_data[UpdateOperator.ADD_TO_SET][k] = {"$each": v}

        if pull_data:
            query_data[UpdateOperator.PULL_ALL] = pull_data

        # if user:
        #     from models.ir_audit_log import IrAuditLog

        #     IrAuditLog().create_log(self, user, "update", query.get("_id"), query_data)
        return self.collection.update_one(query, query_data)

    def update_many(
        self,
        query,
        update_data=None,
        inc_data=None,
        dec_data=None,
        add_to_set_data=None,
        pull_data=None,
    ):
        query_data = {}
        validated_data = {}

        if update_data:
            validated_data = self.validate_data(update_data, partial=True)

            if is_dataclass(validated_data):
                validated_data = self.strip_undeclared_fields(
                    validated_data, update_data.keys()
                )

        validated_data["updated_at"] = datetime.now(timezone.utc)
        query_data[UpdateOperator.SET] = validated_data

        if inc_data:
            query_data[UpdateOperator.INC] = inc_data

        if dec_data:
            dec_data = {k: v * -1 for k, v in dec_data.items()}
            query_data[UpdateOperator.DEC] = dec_data

        if add_to_set_data:
            query_data[UpdateOperator.ADD_TO_SET] = {}
            for k, v in add_to_set_data.items():
                if not isinstance(v, list):
                    v = [v]
                query_data[UpdateOperator.ADD_TO_SET][k] = {"$each": v}

        if pull_data:
            query_data[UpdateOperator.PULL_ALL] = pull_data

        return self.collection.update_many(query, query_data)

    def update_many_different_data(self, data_list):
        """
        data_list = [
            {
                "_id": "66ce781dcbefb7003670c710",
                "set_data": {"name": "Updated Name"},
                "inc_data": {"visit_count": 1},
                "dec_data": {"balance": 5000},
                "add_to_set_data": {"tags": ["premium"]},
                "pull_data": {"tags": ["inactive"]},
            }
        ]
        """
        operations = []
        now = datetime.now(timezone.utc)

        for item in data_list:
            if "_id" not in item:
                continue

            _id = item["_id"]
            if hasattr(self, "type_id") and self.type_id == ParamsValidationType.STRING:
                _id = str(_id)
            else:
                _id = ObjectId(_id)

            update_ops = {"$set": {"updated_at": now}}

            # Gabungkan inc_data dan dec_data ke satu $inc
            combined_inc = {}
            if "inc_data" in item and item["inc_data"]:
                combined_inc.update(item["inc_data"])
            if "dec_data" in item and item["dec_data"]:
                dec_converted = {k: -v for k, v in item["dec_data"].items()}
                combined_inc.update(dec_converted)
            if combined_inc:
                update_ops["$inc"] = combined_inc

            # Tambahkan set_data jika ada
            if "set_data" in item and item["set_data"]:
                update_ops["$set"].update(item["set_data"])

            # add_to_set_data → $addToSet
            if "add_to_set_data" in item and item["add_to_set_data"]:
                update_ops["$addToSet"] = {
                    k: {"$each": v if isinstance(v, list) else [v]}
                    for k, v in item["add_to_set_data"].items()
                }

            # pull_data → $pullAll
            if "pull_data" in item and item["pull_data"]:
                update_ops["$pullAll"] = item["pull_data"]

            operations.append(UpdateOne({"_id": _id}, update_ops))

        if operations:
            result = self.collection.bulk_write(operations)
            return result
        return None

    def upsert_one(self, filter_query: dict, data: dict):
        validated_data = self.validated_and_clean_data(data, partial=True)
        validated_data = self.prepare_common_fields(validated_data, is_new=True)

        result = self.collection.update_one(
            filter_query, {"$set": validated_data}, upsert=True
        )
        return result

    def upsert_many(self, items: list, key_field="_id"):
        operations = []
        for item in items:
            item_dict = asdict(item)

            if key_field not in item_dict:
                continue

            validated_data = self.validated_and_clean_data(item_dict, partial=True)
            validated_data = self.prepare_common_fields(validated_data, is_new=True)

            # -------- new code \\\\
            if "_id" in validated_data:
                validated_data.pop("_id")
            # -------- new code ////
            
            filter_query = {key_field: item_dict[key_field]}
            operations.append(
                UpdateOne(filter_query, {"$set": validated_data}, upsert=True)
            )
        
        if operations:
            result = self.collection.bulk_write(operations)
            return result

        return None

    def find(
        self,
        query={},
        fields=None,
        include_deleted=False,
        convert_to_json=True,
        add_metadata=False,
        query_params={},
        params_validation={},
    ):
        """
        result = model.find(
            add_metadata=True,
            query_params=query_params,
            params_validation=params_validation,
        )
        """
        search = query_params.get("search")
        sort = query_params.get("sort")
        page = query_params.get("page")
        size = query_params.get("size")

        query = DictUtil.merge_dicts(
            query, build_find_query(query_params, params_validation, self.timezone)
        )

        if not include_deleted:
            query["is_deleted"] = False

        if search:
            query["$or"] = [
                {field: {"$regex": search, "$options": "i"}} for field in self.search
            ]

        projection = {}
        if fields:
            for field in fields:
                projection[field] = 1
        else:
            projection = {"is_deleted": 0}

        sort_query = []
        sorting_metadata = []
        if sort:
            for s in sort.split(","):
                field = s[1:] if s.startswith("-") else s
                order = "desc" if s.startswith("-") else "asc"
                direction = -1 if s.startswith("-") else 1
                sort_query.append((field, direction))
                sorting_metadata.append({"field": field, "order": order})
        cursor = self.collection.find(query, projection)
        if sort_query:
            cursor = cursor.sort(sort_query)

        total_records = self.collection.count_documents(query)

        pagination_metadata = {}
        if page is not None and size is not None:
            page = int(page)
            size = int(size)
            skip = (page - 1) * size
            limit = size
            cursor = cursor.skip(skip).limit(limit)

            total_pages = (total_records // size) + (
                1 if total_records % size > 0 else 0
            )
            pagination_metadata = {
                "page": page,
                "size": size,
                "total_pages": total_pages,
                "total_records": total_records,
                "has_next": page < total_pages,
                "has_previous": page > 1,
            }

        result = list(cursor)

        if convert_to_json:
            result = json.loads(json.dumps(result, cls=MongoJSONEncoder))

        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        request_id = str(uuid.uuid4())

        metadata = {
            "pagination": pagination_metadata,
            "timestamp": timestamp,
            "total_records": total_records,
            "request_id": request_id,
            "filters": {
                key: value
                for key, value in query_params.items()
                if key not in ["page", "size", "sort", "search"]
            },
            "sorting": sorting_metadata,
            "additional_info": {
                "note": (
                    "Data hanya mencakup entri yang aktif."
                    if not include_deleted
                    else "Data mencakup semua entri termasuk yang dihapus."
                ),
                "source": "Database production",
            },
        }

        if add_metadata:
            return {"data": result, "metadata": metadata}
        return result

    def find_one(
        self, query=None, fields=None, include_deleted=False, convert_to_json=True
    ):
        query = query or {}
        if not include_deleted:
            query["is_deleted"] = False

        projection = {}
        if fields:
            for field in fields:
                projection[field] = 1
        else:
            projection = {"is_deleted": 0}

        result = self.collection.find_one(query, projection)
        if convert_to_json:
            result = json.loads(json.dumps(result, cls=MongoJSONEncoder))
        return result

    def delete_one(self, query):
        return self.collection.delete_one(query)

    def delete(self, query):
        return self.collection.delete_many(query)

    # def soft_delete(self, query, deleted_data, user=None):
    #     from helpers.security_validator import SecurityValidator

    #     schema_instance = self.schema() if callable(self.schema) else self.schema
    #     fields = schema_instance.fields

    #     timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    #     update_data = {
    #         "is_deleted": True,
    #         "deleted_at": datetime.now(timezone.utc),
    #     }

    #     for key, value in deleted_data.items():
    #         if key == "_id" or not isinstance(value, str):
    #             continue

    #         field_obj = fields.get(key)
    #         has_enum = False

    #         if field_obj and field_obj.validate:
    #             validators = field_obj.validate
    #             if not isinstance(validators, (list, tuple)):
    #                 validators = [validators]
    #             has_enum = any(isinstance(v, OneOf) for v in validators)

    #         if not has_enum:
    #             update_data[key] = f"{value}_{timestamp}"

    #     audit_logger.info(
    #         f"[DELETE] collection={self.collection_name} user={getattr(user, 'username', 'unknown')} query={query}"
    #     )

    #     return self.collection.update_one(query, {"$set": update_data})

    def soft_delete(self, query, deleted_data, user=None):
        from helpers.security_validator import SecurityValidator

        update_data = {
            "is_deleted": True,
            "deleted_at": datetime.now(timezone.utc),
        }
        schema_instance = self.schema()
        schema_fields = schema_instance.fields
        for key, value in deleted_data.items():
            if key not in SecurityValidator.IMMUTABLE_FIELDS:
                field = schema_fields.get(key)
                if (
                    isinstance(value, str)
                    and field
                    and not isinstance(field.validate, OneOf)
                ):
                    update_data[key] = (
                        f"{value}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
                    )

        # if user:
        #     from models.ir_audit_log import IrAuditLog

        #     IrAuditLog().create_log(
        #         self, user, "delete", query.get("_id"), deleted_data
        #     )
        return self.collection.update_one(query, {"$set": update_data})

    # def soft_delete_many(self, _ids: list, user=None):
    #     from utils.string_util import StringUtil

    #     timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    #     update_data = {
    #         "is_deleted": True,
    #         "deleted_at": datetime.now(timezone.utc),
    #     }

    #     documents = list(self.collection.find({"_id": {"$in": _ids}}))
    #     for doc in documents:
    #         for key, value in doc.items():
    #             if key != "_id" and isinstance(value, str):
    #                 update_data[key] = (
    #                     f"{value}_{timestamp}_{StringUtil.generate_code('nnccnncc')}"
    #                 )

    #     result = self.collection.update_many(
    #         {"_id": {"$in": _ids}}, {"$set": update_data}
    #     )

    #     audit_logger.info(
    #         f"[SOFT_DELETE_MANY] collection={self.collection_name} user={user.username if user else 'anonymous'} _ids={[str(i) for i in _ids]}"
    #     )

    #     return result


# -----------------------------------------------------------------
    # ------------- old code ////
    # def soft_delete_many(self, query):
    #     from utils.string_util import StringUtil

    #     timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    #     update_data = {
    #         "is_deleted": True,
    #         "deleted_at": datetime.now(timezone.utc),
    #     }

    #     documents = list(self.collection.find(query))
    #     for doc in documents:
    #         for key, value in doc.items():
    #             if key != "_id" and isinstance(value, str):
    #                 update_data[key] = (
    #                     f"{value}_{timestamp}_{StringUtil.generate_code('nnccnncc')}"
    #                 )

    #     result = self.collection.update_many(query, {"$set": update_data})
    #     return result
    # ------------- old code ////
    
    # ------ new code \\\
    def soft_delete_many(self, query):
        from helpers.security_validator import SecurityValidator
        from utils.string_util import StringUtil

        schema_instance = self.schema()
        schema_fields = schema_instance.fields
        documents = list(self.collection.find(query))
        data_list = []
        for doc in documents:
            update_data = {
                "is_deleted": True,
                "deleted_at": datetime.now(timezone.utc),
            }
            for key, value in doc.items():
                if key not in SecurityValidator.IMMUTABLE_FIELDS:
                    field = schema_fields.get(key)
                    if (
                        isinstance(value, str)
                        and field
                        and not isinstance(field.validate, OneOf)
                    ):
                        update_data[key] = (
                            f"{value}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
                        )
            data_list.append({
                "_id": doc["_id"],
                "set_data": update_data,
            })
            
        self.update_many_different_data(data_list)

    # ------ new code ///
# -----------------------------------------------------------------



    def aggregate(
        self,
        query={},
        fields=None,  # id,name,no_lookup
        convert_to_json=True,
        add_metadata=False,
        include_deleted=False,
        query_params={},
        params_validation={},
        lookup=[],
        additional_fields={},
        group={},
        exclude=None,  # student_ids,modules
    ):
        """
        result = model.aggregate(
            add_metadata=True,
            query_params=query_params,
            params_validation=params_validation,
            lookup=[
                "job",
                "job_grade",
                "department",
                "user",
                "partner",
                "employee_job->job,employee",
            ],
            additional_fields={
                "complete_address": {
                    "type": FieldType.CONCAT,
                    "value": [
                        "$address.street",
                        " Ds. ",
                        "$address.village",
                        " Kec. ",
                        "$address.district",
                        " ",
                        "$address.city",
                        " ",
                        "$address.province",
                        ", ",
                        "$address.zipcode",
                    ],
                },
                "student": {
                    "type": FieldType.SWITCH,
                    "value": {
                        "branches": [
                            {"case": {"$eq": ["$bank_id", "bsi"]}, "then": "$student_bsi_info"},
                            {"case": {"$eq": ["$bank_id", "sbi"]}, "then": "$student_sbi_info"},
                            {"case": {"$eq": ["$bank_id", "nano"]}, "then": "$student_nano_info"},
                        ],
                        "default": {}
                    }
                }
            },
            group={
                "_id": {
                    "grade_id": "$grade_id",
                    "grade_name": "$demo_author_grade_info.name",
                },
                "aggregation": {"$salary": [[UpdateOperator.GROUP_AVG, 0], [UpdateOperator.GROUP_SUM, 0]]},
            },
        )
        """

        search = query_params.get("search")
        sort = query_params.get("sort")
        page = query_params.get("page")
        size = query_params.get("size")

        query = DictUtil.merge_dicts(
            query, build_find_query(query_params, params_validation, self.timezone)
        )
        if not include_deleted:
            query["is_deleted"] = False

        if search:
            query["$or"] = [
                {field: {"$regex": search, "$options": "i"}} for field in self.search
            ]

        sort_dict = {}
        sorting_metadata = []
        if sort:
            for field in sort.split(","):
                if field.startswith("-"):
                    sort_dict[field[1:]] = -1
                    order = "desc"
                    field_name = field[1:]
                else:
                    sort_dict[field] = 1
                    order = "asc"
                    field_name = field
                sorting_metadata.append({"field": field_name, "order": order})

        total_records = self.collection.count_documents(query)
        pipeline = []
        if fields:
            fields = fields.split(",")
            schema_fields = [k for k, v in self.schema._declared_fields.items()]
            missing_fields = [item for item in schema_fields if item not in fields]
            project = {}
            for i in missing_fields:
                project[i] = 0
            pipeline.append({"$project": project})
        if query:
            pipeline.append({"$match": query})
        if sort_dict:
            pipeline.append({"$sort": sort_dict})

        pagination_metadata = {}
        if page is not None and size is not None:
            page = int(page)
            size = int(size)
            skip = (page - 1) * size
            pipeline.append({"$skip": skip})
            pipeline.append({"$limit": size})
            total_pages = (total_records // size) + (
                1 if total_records % size > 0 else 0
            )
            pagination_metadata = {
                "page": page,
                "size": size,
                "total_pages": total_pages,
                "total_records": total_records,
                "has_next": page < total_pages,
                "has_previous": page > 1,
            }
        if not fields:
            fields = ["___"]
        if fields and "no_lookup" not in fields:
            pipeline.extend(self.add_lookup(lookup))
            pipeline.append({"$project": {"is_deleted": 0}})
            # additional_fields = self.add_field(additional_fields)
            # if additional_fields:
            #     for k, v in additional_fields.items():
            #         pipeline.append({"$addFields": {k: v}})
            additional_fields = self.add_field(additional_fields)
            project_removal = {}

            for k in list(additional_fields.keys()):
                if k.startswith("__remove__:"):
                    old_field = k.replace("__remove__:", "")
                    project_removal[old_field] = 0
                    del additional_fields[k]
            if additional_fields:
                pipeline.append({"$addFields": additional_fields})
            if project_removal:
                pipeline.append({"$project": project_removal})

        if group:
            group_query = {}
            project_query = {
                "_id": 1,
                "count_data": 1,
            }
            if len(group["_id"]) == 1:
                first_key, first_value = next(iter(group["_id"].items()))
                group_query["_id"] = first_value
            else:
                group_query["_id"] = group["_id"]
            group_query["count_data"] = {"$sum": 1}
            for k, v in group["aggregation"].items():
                for i in v:
                    group_query[f"{i[0]}_{k[1:]}"] = {f"${i[0]}": k}
                    project_query[f"{i[0]}_{k[1:]}"] = 1
                    if i[1] > -1:
                        project_query[f"{i[0]}_{k[1:]}"] = {
                            "$round": [f"${i[0]}_{k[1:]}", i[1]]
                        }
            pipeline.append({"$group": group_query})
            pipeline.append({"$project": project_query})

        if exclude:
            exclude = exclude.split(",")
            project = {}
            for i in exclude:
                project[i] = 0
            pipeline.append({"$project": project})
        result = list(self.collection.aggregate(pipeline))
        if convert_to_json:
            result = json.loads(json.dumps(result, cls=MongoJSONEncoder))

        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        request_id = str(uuid.uuid4())

        metadata = {
            "pagination": pagination_metadata,
            "timestamp": timestamp,
            "total_records": total_records,
            "request_id": request_id,
            "filters": {
                key: value
                for key, value in query_params.items()
                if key not in ["page", "size", "sort", "search"]
            },
            "sorting": sorting_metadata,
            "additional_info": {
                "note": (
                    "Data hanya mencakup entri yang aktif."
                    if not include_deleted
                    else "Data mencakup semua entri termasuk yang dihapus."
                ),
                "source": "Database production",
            },
        }

        if add_metadata:
            return {"data": result, "metadata": metadata}
        return result

    # def add_lookup(self, lookup):
    #     pipeline = []
    #     for i in lookup:
    #         split = i.split("->")
    #         nested_field = []
    #         main_field = split[0]
    #         if len(split) == 2:
    #             nested_field = split[1].split(",")

    #         if main_field not in self.foreign_key:
    #             continue
    #         fk = self.foreign_key[main_field]
    #         model_cls = fk["model"]() if callable(fk["model"]) else fk["model"]
    #         collection_name = model_cls.collection_name
    #         field_type = self.schema._declared_fields.get(fk["local"])
    #         sort_config = fk.get("sort")
    #         if sort_config:
    #             sort_fields = sort_config.split(",")
    #             sort_dict = {
    #                 field.lstrip("-"): -1 if field.startswith("-") else 1
    #                 for field in sort_fields
    #             }

    #             lookup_pipeline = [
    #                 {
    #                     "$match": {
    #                         "$expr": (
    #                             {"$in": [f"${fk['foreign']}", "$$local_id"]}
    #                             if (
    #                                 isinstance(field_type, ObjectIdsField)
    #                                 or isinstance(field_type, fields.List)
    #                             )
    #                             else {"$eq": [f"${fk['foreign']}", "$$local_id"]}
    #                         )
    #                     }
    #                 },
    #                 {"$sort": sort_dict},
    #             ]

    #             pipeline.append(
    #                 {
    #                     "$lookup": {
    #                         "from": collection_name,
    #                         "let": {"local_id": f"${fk['local']}"},
    #                         "pipeline": lookup_pipeline,
    #                         # "as": f"{collection_name}_info",
    #                         "as": f"{main_field}_info",
    #                     }
    #                 }
    #             )
    #         else:
    #             lookup_pipeline = [
    #                 {
    #                     "$match": {
    #                         "$expr": (
    #                             {"$in": [f"${fk['foreign']}", "$$local_id"]}
    #                             if (
    #                                 isinstance(field_type, ObjectIdsField)
    #                                 or isinstance(field_type, fields.List)
    #                             )
    #                             else {"$eq": [f"${fk['foreign']}", "$$local_id"]}
    #                         )
    #                     }
    #                 }
    #             ]

    #             pipeline.append(
    #                 {
    #                     "$lookup": {
    #                         "from": collection_name,
    #                         "let": {"local_id": f"${fk['local']}"},
    #                         "pipeline": lookup_pipeline,
    #                         "as": f"{main_field}_info",
    #                     }
    #                 }
    #             )

    #         pipeline.append(
    #             {
    #                 "$addFields": {
    #                     f"{main_field}_info": {
    #                         "$cond": {
    #                             "if": {"$eq": [f"${fk['local']}", None]},
    #                             "then": None,
    #                             "else": f"${main_field}_info",
    #                         }
    #                     }
    #                 }
    #             }
    #         )

    #         should_unwind = (
    #             fk.get("relation") == RelationType.ONE_TO_ONE
    #         ) or isinstance(field_type, (ObjectIdField, fields.Str))

    #         if should_unwind:
    #             pipeline.append(
    #                 {
    #                     "$unwind": {
    #                         "path": f"${main_field}_info",
    #                         "preserveNullAndEmptyArrays": True,
    #                     }
    #                 }
    #             )

    #         pipeline.append(
    #             {
    #                 "$project": {
    #                     f"{main_field}_info.is_deleted": 0,
    #                     f"{main_field}_info.created_at": 0,
    #                     f"{main_field}_info.updated_at": 0,
    #                 }
    #             }
    #         )

    #         for j in nested_field:
    #             model_cls = fk["model"]() if callable(fk["model"]) else fk["model"]
    #             collection_name = model_cls.collection_name
    #             nested_fk = model_cls.foreign_key[j]
    #             nested_model_cls = (
    #                 nested_fk["model"]()
    #                 if callable(nested_fk["model"])
    #                 else nested_fk["model"]
    #             )
    #             nested_collection_name = nested_model_cls.collection_name
    #             pipeline.extend(
    #                 [
    #                     {
    #                         "$lookup": {
    #                             "from": nested_collection_name,
    #                             "localField": f"{main_field}_info.{nested_fk['local']}",
    #                             "foreignField": nested_fk["foreign"],
    #                             "as": f"{j}_info",
    #                         }
    #                     },
    #                     {
    #                         "$project": {
    #                             f"{j}_info.is_deleted": 0,
    #                             f"{j}_info.created_at": 0,
    #                             f"{j}_info.updated_at": 0,
    #                         }
    #                     },
    #                 ]
    #             )

    #             if should_unwind:
    #                 pipeline.extend(
    #                     [
    #                         {
    #                             "$unwind": {
    #                                 "path": f"${j}_info",
    #                                 "preserveNullAndEmptyArrays": True,
    #                             }
    #                         },
    #                         {
    #                             "$addFields": {
    #                                 f"{main_field}_info.{j}_info": f"${j}_info"
    #                             }
    #                         },
    #                         {"$project": {f"{j}_info": 0}},
    #                     ]
    #                 )
    #             else:
    #                 pipeline.extend(
    #                     [
    #                         {
    #                             "$addFields": {
    #                                 f"{main_field}_info": {
    #                                     "$map": {
    #                                         "input": f"${main_field}_info",
    #                                         "as": "obj",
    #                                         "in": {
    #                                             "$mergeObjects": [
    #                                                 "$$obj",
    #                                                 {
    #                                                     f"{j}_info": {
    #                                                         "$arrayElemAt": [
    #                                                             f"${j}_info",
    #                                                             {
    #                                                                 "$indexOfArray": [
    #                                                                     f"${j}_info._id",
    #                                                                     f"$$obj.{j}",
    #                                                                 ]
    #                                                             },
    #                                                         ]
    #                                                     }
    #                                                 },
    #                                             ]
    #                                         },
    #                                     }
    #                                 }
    #                             }
    #                         },
    #                         {"$project": {f"{nested_collection_name}_info": 0}},
    #                     ]
    #                 )
    #     return pipeline

    def add_lookup(self, lookup):
        pipeline = []
        for i in lookup:
            split = i.split("->")
            nested_field = []
            main_field = split[0]
            if len(split) == 2:
                nested_field = split[1].split(",")

            if main_field not in self.foreign_key:
                continue

            fk = self.foreign_key[main_field]
            model_cls = fk["model"]() if callable(fk["model"]) else fk["model"]
            collection_name = model_cls.collection_name
            field_type = self.schema._declared_fields.get(fk["local"])
            sort_config = fk.get("sort")

            main_project = {
                f"{main_field}_info.is_deleted": 0,
                f"{main_field}_info.created_at": 0,
                f"{main_field}_info.updated_at": 0,
            }
            fields_list = [k for k, v in model_cls.schema._declared_fields.items()]
            if fk.get("fields"):
                hidden = [
                    field for field in fields_list if field not in fk.get("fields")
                ]
                for i in hidden:
                    main_project[f"{main_field}_info.{i}"] = 0

            match_expr = {
                "$and": [
                    (
                        {"$in": [f"${fk['foreign']}", "$$local_id"]}
                        if isinstance(field_type, (ObjectIdsField, fields.List))
                        else {"$eq": [f"${fk['foreign']}", "$$local_id"]}
                    ),
                    {"$eq": ["$is_deleted", False]},
                ]
            }

            lookup_pipeline = [{"$match": {"$expr": match_expr}}]

            if sort_config:
                sort_fields = sort_config.split(",")
                sort_dict = {
                    field.lstrip("-"): -1 if field.startswith("-") else 1
                    for field in sort_fields
                }
                lookup_pipeline.append({"$sort": sort_dict})

            pipeline.append(
                {
                    "$lookup": {
                        "from": collection_name,
                        "let": {"local_id": f"${fk['local']}"},
                        "pipeline": lookup_pipeline,
                        "as": f"{main_field}_info",
                    }
                }
            )

            pipeline.append(
                {
                    "$addFields": {
                        f"{main_field}_info": {
                            "$cond": {
                                "if": {"$eq": [f"${fk['local']}", None]},
                                "then": None,
                                "else": f"${main_field}_info",
                            }
                        }
                    }
                }
            )

            should_unwind = (
                fk.get("relation") == RelationType.ONE_TO_ONE
            ) or isinstance(field_type, (ObjectIdField, fields.Str))

            if should_unwind:
                pipeline.append(
                    {
                        "$unwind": {
                            "path": f"${main_field}_info",
                            "preserveNullAndEmptyArrays": True,
                        }
                    }
                )

            pipeline.append({"$project": main_project})

            for j in nested_field:
                nested_fk = model_cls.foreign_key[j]
                nested_model_cls = (
                    nested_fk["model"]()
                    if callable(nested_fk["model"])
                    else nested_fk["model"]
                )
                nested_collection_name = nested_model_cls.collection_name

                pipeline.append(
                    {
                        "$lookup": {
                            "from": nested_collection_name,
                            "let": {
                                "local_id": f"${main_field}_info.{nested_fk['local']}"
                            },
                            "pipeline": [
                                {
                                    "$match": {
                                        "$expr": {
                                            "$and": [
                                                {
                                                    "$eq": [
                                                        f"${nested_fk['foreign']}",
                                                        "$$local_id",
                                                    ]
                                                },
                                                {"$eq": ["$is_deleted", False]},
                                            ]
                                        }
                                    }
                                },
                                {
                                    "$project": {
                                        "is_deleted": 0,
                                        "created_at": 0,
                                        "updated_at": 0,
                                    }
                                },
                            ],
                            "as": f"{j}_info",
                        }
                    }
                )

                if should_unwind:
                    pipeline.extend(
                        [
                            {
                                "$unwind": {
                                    "path": f"${j}_info",
                                    "preserveNullAndEmptyArrays": True,
                                }
                            },
                            {
                                "$addFields": {
                                    f"{main_field}_info.{j}_info": f"${j}_info"
                                }
                            },
                            {"$project": {f"{j}_info": 0}},
                        ]
                    )
                else:
                    pipeline.extend(
                        [
                            {
                                "$addFields": {
                                    f"{main_field}_info": {
                                        "$map": {
                                            "input": f"${main_field}_info",
                                            "as": "obj",
                                            "in": {
                                                "$mergeObjects": [
                                                    "$$obj",
                                                    {
                                                        f"{j}_info": {
                                                            "$arrayElemAt": [
                                                                f"${j}_info",
                                                                {
                                                                    "$indexOfArray": [
                                                                        f"${j}_info._id",
                                                                        f"$$obj.{j}",
                                                                    ]
                                                                },
                                                            ]
                                                        }
                                                    },
                                                ]
                                            },
                                        }
                                    }
                                }
                            },
                            {"$project": {f"{j}_info": 0}},
                        ]
                    )
        return pipeline

    # def add_field(self, _additional_fields):
    #     additional_fields = {}
    #     for k, v in _additional_fields.items():
    #         if v["type"] == FieldType.CONCAT:
    #             additional_fields[k] = {"$concat": v["value"]}
    #         elif v["type"] == FieldType.DATE_TO_STRING:
    #             additional_fields[f"{k}"] = {
    #                 "$dateToString": {"format": "%d-%m-%Y", "date": v["value"]}
    #             }
    #         elif v["type"] == FieldType.TIME:
    #             additional_fields[f"{k}"] = {
    #                 "$dateToString": {"format": "%H:%M:%S", "date": v["value"]}
    #             }
    #         elif v["type"] == FieldType.HOUR:
    #             additional_fields[f"{k}"] = {"$hour": v["value"]}
    #         elif v["type"] == FieldType.MINUTE:
    #             additional_fields[f"{k}"] = {"$minute": v["value"]}
    #         elif v["type"] == FieldType.SECOND:
    #             additional_fields[f"{k}"] = {"$second": v["value"]}
    #         elif v["type"] == FieldType.DAY:
    #             additional_fields[f"{k}"] = {"$dayOfMonth": v["value"]}
    #         elif v["type"] == FieldType.MONTH:
    #             additional_fields[f"{k}"] = {"$month": v["value"]}
    #         elif v["type"] == FieldType.YEAR:
    #             additional_fields[f"{k}"] = {"$year": v["value"]}
    #         elif v["type"] == FieldType.DIFF_DAYS_FROM_TODAY:
    #             today = datetime.now(timezone.utc).astimezone().date()
    #             today_datetime = datetime(
    #                 today.year, today.month, today.day, tzinfo=timezone.utc
    #             )
    #             additional_fields[f"{k}"] = {
    #                 "$toInt": {
    #                     "$divide": [
    #                         {
    #                             "$subtract": [
    #                                 today_datetime,
    #                                 {
    #                                     "$dateFromString": {
    #                                         "dateString": {
    #                                             "$dateToString": {
    #                                                 "format": "%Y-%m-%d",
    #                                                 "date": v["value"],
    #                                             }
    #                                         }
    #                                     }
    #                                 },
    #                             ]
    #                         },
    #                         86400000,
    #                     ]
    #                 }
    #             }
    #         elif v["type"] == FieldType.DAY_OF_WEEK:
    #             additional_fields[f"{k}"] = {"$dayOfWeek": v["value"]}
    #         elif v["type"] == FieldType.DAY_OF_MONTH:
    #             additional_fields[f"{k}"] = {
    #                 "$toInt": {
    #                     "$ceil": {
    #                         "$divide": [
    #                             {"$subtract": [{"$dayOfMonth": v["value"]}, 1]},
    #                             7,
    #                         ]
    #                     }
    #                 }
    #             }
    #         elif v["type"] == FieldType.SUM:
    #             additional_fields[f"{k}"] = {"$sum": v["value"]}
    #         elif v["type"] == FieldType.SUBTRACT:
    #             additional_fields[f"{k}"] = {"$subtract": v["value"]}
    #         elif v["type"] == FieldType.MULTIPLY:
    #             additional_fields[f"{k}"] = {"$multiply": v["value"]}
    #         elif v["type"] == FieldType.MULTIPLY_WITH_CONSTANT:
    #             if not isinstance(v["value"][1], (int, float)):
    #                 raise ValueError(
    #                     "Untuk MULTIPLY_WITH_CONSTANT, `extra` harus berupa angka."
    #                 )
    #             additional_fields[f"{k}"] = {"$multiply": v["value"]}
    #         elif v["type"] == FieldType.DIVIDE:
    #             additional_fields[f"{k}"] = {"$divide": v["value"]}
    #         elif v["type"] == FieldType.DIVIDE_WITH_CONSTANT:
    #             if not isinstance(v["value"][1], (int, float)):
    #                 raise ValueError(
    #                     "Untuk DIVIDE_WITH_CONSTANT, `extra` harus berupa angka."
    #                 )
    #             additional_fields[f"{k}"] = {"$divide": v["value"]}
    #         elif v["type"] == FieldType.ROUND:
    #             if not isinstance(v["value"][1], (int, float)):
    #                 raise ValueError("Untuk ROUND, `extra` harus berupa angka.")
    #             additional_fields[f"{k}"] = {"$round": v["value"]}
    #         elif v["type"] == FieldType.FORMAT_NUMBER:
    #             additional_fields[f"{k}"] = {
    #                 "$function": {
    #                     "body": "function(num) { return num.toLocaleString('en-US'); }",
    #                     "args": [v["value"]],
    #                     "lang": "js",
    #                 }
    #             }
    #         elif v["type"] == FieldType.STRING_LENGTH:
    #             additional_fields[f"{k}"] = {"$strLenCP": v["value"]}
    #         elif v["type"] == FieldType.UPPERCASE:
    #             additional_fields[f"{k}"] = {"$toUpper": v["value"]}
    #         elif v["type"] == FieldType.LOWERCASE:
    #             additional_fields[f"{k}"] = {"$toLower": v["value"]}
    #         elif v["type"] == FieldType.TRIM:
    #             additional_fields[f"{k}"] = {"$trim": {"input": v["value"]}}
    #         elif v["type"] == FieldType.LTRIM:
    #             additional_fields[f"{k}"] = {"$ltrim": {"input": v["value"]}}
    #         elif v["type"] == FieldType.RTRIM:
    #             additional_fields[f"{k}"] = {"$rtrim": {"input": v["value"]}}
    #         elif v["type"] == FieldType.REPLACE_STRING:
    #             additional_fields[f"{k}"] = {
    #                 "$replaceAll": {
    #                     "input": v["value"][0],
    #                     "find": v["value"][1],
    #                     "replacement": v["value"][2],
    #                 }
    #             }
    #         elif v["type"] == FieldType.SPLIT_STRING:
    #             additional_fields[f"{k}"] = {"$split": v["value"]}
    #         elif v["type"] == FieldType.ARRAY_LENGTH:
    #             additional_fields[f"{k}"] = {"$size": v["value"]}
    #         elif v["type"] == FieldType.ELEMENT:
    #             additional_fields[f"{k}"] = {"$arrayElemAt": v["value"]}
    #         elif v["type"] == FieldType.ARRAY_SLICE:
    #             additional_fields[f"{k}"] = {"$slice": v["value"]}
    #         elif v["type"] == FieldType.SUM_FROM_ARRAY_DICT:
    #             additional_fields[f"{k}"] = {
    #                 "$sum": {
    #                     "$map": {
    #                         "input": v["value"][0],
    #                         "as": "element",
    #                         "in": f"$$element.{ v['value'][0]}",
    #                     }
    #                 }
    #             }
    #         elif v["type"] == FieldType.AVG_FROM_ARRAY_DICT:
    #             additional_fields[f"{k}"] = {
    #                 "$avg": {
    #                     "$map": {
    #                         "input": v["value"][0],
    #                         "as": "element",
    #                         "in": f"$$element.{ v['value'][0]}",
    #                     }
    #                 }
    #             }
    #         elif v["type"] == FieldType.SUM_FROM_ARRAY:
    #             additional_fields[f"{k}"] = {"$sum": v["value"]}
    #         elif v["type"] == FieldType.AVG_FROM_ARRAY:
    #             additional_fields[f"{k}"] = {"$avg": v["value"]}
    #         elif v["type"] == FieldType.CONCAT_FROM_ARRAY_DICT:
    #             additional_fields[f"{k}"] = {
    #                 "$reduce": {
    #                     "input": v["value"][0],
    #                     "initialValue": "",
    #                     "in": {
    #                         "$concat": [
    #                             "$$value",
    #                             {
    #                                 "$cond": [
    #                                     {"$eq": ["$$value", ""]},
    #                                     "",
    #                                     v["value"][2],
    #                                 ]
    #                             },
    #                             f"$$this.{v['value'][1]}",
    #                         ]
    #                     },
    #                 }
    #             }
    #         elif v["type"] == FieldType.CONCAT_FROM_ARRAY:
    #             additional_fields[f"{k}"] = {
    #                 "$reduce": {
    #                     "input": v["value"],
    #                     "initialValue": "",
    #                     "in": {
    #                         "$concat": [
    #                             {"$cond": [{"$eq": ["$$value", ""]}, "", ", "]},
    #                             "$$this",
    #                         ]
    #                     },
    #                 }
    #             }
    #         elif v["type"] == FieldType.ARRAY_FILTER:
    #             additional_fields[f"{k}"] = {
    #                 "$filter": {
    #                     "input": v["value"][0],
    #                     "as": "item",
    #                     "cond": v["value"][1],
    #                 }
    #             }
    #         elif v["type"] == FieldType.CAST_INT:
    #             additional_fields[f"{k}"] = {"$toInt": v["value"]}
    #         elif v["type"] == FieldType.CAST_STRING:
    #             additional_fields[f"{k}"] = {"$toString": v["value"]}
    #         elif v["type"] == FieldType.RENAME_FIELD:
    #             if not isinstance(v["value"], list) or len(v["value"]) != 1:
    #                 raise ValueError(
    #                     "Untuk RENAME_FIELD, value harus berupa list dengan 1 elemen nama field lama."
    #                 )
    #             old_field = v["value"][0]
    #             additional_fields[k] = f"${old_field}"
    #             additional_fields[f"__remove__:{old_field}"] = "__remove__"
    #         elif v["type"] == FieldType.SWITCH:
    #             if not isinstance(v["value"], dict):
    #                 raise ValueError("Value untuk SWITCH harus berupa dict.")

    #             # format: {"branches": [...], "default": ...}
    #             branches = []
    #             for condition in v["value"].get("branches", []):
    #                 if "case" not in condition or "then" not in condition:
    #                     raise ValueError(
    #                         "Setiap branch pada SWITCH harus memiliki 'case' dan 'then'."
    #                     )
    #                 branches.append(
    #                     {"case": condition["case"], "then": condition["then"]}
    #                 )
    #             switch_expr = {
    #                 "$switch": {
    #                     "branches": branches,
    #                     "default": v["value"].get("default", None),
    #                 }
    #             }
    #             additional_fields[f"{k}"] = switch_expr

    #     return additional_fields

    def add_field(self, _additional_fields):
        additional_fields = {}

        for key, config in _additional_fields.items():
            field_type = config["type"]
            value = config["value"]

            if field_type not in registry:
                raise ValueError(f"FieldType '{field_type}' belum didukung.")

            handler = registry[field_type]

            if field_type == "RENAME_FIELD":
                result, old_field = handler(value)
                additional_fields[key] = result
                additional_fields[f"__remove__:{old_field}"] = "__remove__"
            else:
                additional_fields[key] = handler(value)

        return additional_fields

    def validate_ids_exist(self, ids, id_field="_id"):
        if not ids:
            return

        found_ids = self.collection.distinct(id_field, {id_field: {"$in": ids}})
        not_found = list(set(ids) - set(found_ids))

        if not_found:
            raise ValidationError(
                f"ID berikut tidak ditemukan di koleksi {self.collection_name}: {not_found}"
            )

    def sync_one(self, document_id):
        if hasattr(self, "type_id") and self.type_id == ParamsValidationType.STRING:
            document_id = str(document_id)
        else:
            document_id = ObjectId(document_id)

        doc = self.collection.find_one({"_id": document_id})
        if not doc:
            raise ValueError(f"Dokumen dengan _id {document_id} tidak ditemukan.")

        schema_fields = set(self.schema().fields.keys())
        allowed_fields = schema_fields.union(
            {"_id", "created_at", "updated_at", "is_deleted"}
        )

        extra_fields = set(doc.keys()) - allowed_fields
        if not extra_fields:
            return {"status": "ok", "message": "No extra fields to remove."}

        unset_fields = {field: "" for field in extra_fields}
        self.collection.update_one({"_id": document_id}, {"$unset": unset_fields})

        audit_logger.info(
            f"[SYNC_ONE] collection={self.collection_name} _id={document_id} removed_fields={list(extra_fields)}"
        )
        return {
            "status": "synced",
            "document_id": str(document_id),
            "removed_fields": list(extra_fields),
        }

    def sync_all(self, include_deleted=False, default={}):
        schema_fields = set(self.schema().fields.keys())
        allowed_fields = schema_fields.union(
            {"_id", "created_at", "updated_at", "is_deleted"}
        )

        query = {} if include_deleted else {"is_deleted": False}
        cursor = self.collection.find(query, {"_id": 1})

        total_synced = 0
        total_removed_fields = 0
        total_missing_fields = 0
        all_removed_fields = set()
        all_missing_fields = set()

        for doc in cursor:
            document_id = doc["_id"]
            full_doc = self.collection.find_one({"_id": document_id})
            if not full_doc:
                continue

            full_doc_fields = set(full_doc.keys())
            extra_fields = full_doc_fields - allowed_fields
            missing_fields = allowed_fields - full_doc_fields

            set_fields = {}
            for field in missing_fields:
                set_fields[field] = default.get(field, None)

            if set_fields:
                self.collection.update_one({"_id": document_id}, {"$set": set_fields})
                audit_logger.info(
                    f"[SYNC_ALL][SET] collection={self.collection_name} _id={document_id} missing_fields={list(missing_fields)}"
                )
                total_missing_fields += len(missing_fields)
                all_missing_fields.update(missing_fields)

            unset_fields = {}
            if extra_fields:
                unset_fields = {field: "" for field in extra_fields}
                self.collection.update_one(
                    {"_id": document_id}, {"$unset": unset_fields}
                )
                audit_logger.info(
                    f"[SYNC_ALL][UNSET] collection={self.collection_name} _id={document_id} removed_fields={list(extra_fields)}"
                )
                total_removed_fields += len(extra_fields)
                all_removed_fields.update(extra_fields)

            if extra_fields or set_fields:
                total_synced += 1

        return {
            "status": "done",
            "total_synced_docs": total_synced,
            "total_removed_fields": total_removed_fields,
            "total_missing_fields": total_missing_fields,
            "unique_fields_removed": sorted(all_removed_fields),
            "unique_fields_added": sorted(all_missing_fields),
        }


"""
Contoh Penggunaan:

# INSERT
book = {
    "title": "Belajar MongoDB",
    "author_id": "64af9a3c3c8c3bd9820d1a56",
}
BookModel().insert_one(book)

# FIND
BookModel().find(query_params={"search": "mongo", "page": 1, "size": 10})

# UPDATE
BookModel().update_one(
    {"_id": ObjectId("64af9a3c3c8c3bd9820d1a56")},
    update_data={"title": "MongoDB for Beginners"}
)

# SOFT DELETE
BookModel().soft_delete({"_id": ObjectId(...)}, {"title": "MongoDB for Beginners"})

# AGGREGATION (dengan lookup dan additional_fields)
BookModel().aggregate(
    query_params={"search": "mongo"},
    lookup=["author_id"],
    additional_fields={
        "formatted_title": {
            "type": FieldType.CONCAT,
            "value": ["Mongo: ", "$title"]
        }
    },
    group={
        "_id": {"author_id": "$author_id"},
        "aggregation": {"$rating": [[GroupAggregationOp.GROUP_AVG, 1]]}
    }
)
"""
