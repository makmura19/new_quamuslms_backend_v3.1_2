from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from bson import ObjectId
from models.edu_academic_year import EduAcademicYear
from models.school_class import SchoolClass
from models.finance_invoice_type import FinanceInvoiceType
from models.finance_invoice_price import FinanceInvoicePrice
from models.school_student import SchoolStudent
from utils.string_util import StringUtil
from models.finance_invoice import FinanceInvoiceData
from utils.today import indonesian_months


class MainService(BaseService):
   
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
        )
        return result


    @staticmethod
    def student(
        model: BaseModel, query_params, params_validation, user, headers_dict=None
    ):
        if (
            not query_params.get("school_id")
            or not query_params.get("academic_year_id")
            or not query_params.get("class_id")
            or not query_params.get("type_id")
        ):
            raise ValidationError("Quert params not complete.")
        
        school_id = ObjectId(query_params.get("school_id"))
        academic_year_id = ObjectId(query_params.get("academic_year_id"))
        class_id = ObjectId(query_params.get("class_id"))
        type_id = ObjectId(query_params.get("type_id"))
        
        class_data = SchoolClass().find_one({"_id":class_id,"school_id":school_id,})
        if not class_data:
            raise ValidationError("Class data not found")
        invoice_type_data = FinanceInvoiceType().find_one({"_id":type_id,"school_id":school_id,})
        if not invoice_type_data:
            raise ValidationError("Invoice Type not found")
        student_data = SchoolStudent().aggregate(
            add_metadata=False,
            query={"school_id":school_id,"class_id":class_id,},
            query_params={"sort": "name"},
            lookup=["class"],
        )

        query = {"school_id":school_id,"academic_year_id":academic_year_id,"class_id":class_id,"type_id":type_id,}
        if invoice_type_data.get("type") == "month":
            if not query_params.get("month"):
                return {"data": []}
            query["month"] = int(query_params.get("month"))
        if invoice_type_data.get("type") == "semester":
            if not query_params.get("semester_id"):
                return {"data": []}
            query["semester_id"] = query_params.get("semester_id")

        invoice_price_data = FinanceInvoicePrice().aggregate(
            {
                "school_id": school_id,
                "type_id": type_id,
                "level_id": ObjectId(class_data.get("level_id")),
            },
            lookup=["variants"],
        )
        if not invoice_price_data:
            return {"data": []}
        invoice_price_data = invoice_price_data[0]
        variant_list = invoice_price_data.get("variants_info", [])
        
        invoice_student_data = model.find(query)
        invoice_student_data = {
            item.get("student_id"):item for item in invoice_student_data
        }

        data = []
        generated_ids = []
        for i in student_data:
            variant_id = None
            amount = invoice_price_data.get("amount")
            criteria = {
                "gender": i.get("gender"),
                "is_boarding": i.get("is_boarding"),
                "is_alumni": i.get("is_alumni"),
                # "class_type": i.get("class_type"),
                "degree_id": i.get("degree_id"),
                "major_id": i.get("major_id"),
                "program_id": i.get("program_id"),
            }

            for variant in variant_list:
                match = True
                for key, value in criteria.items():
                    if (
                        key in variant
                        and variant[key] != None
                        and variant[key] != value
                    ):
                        match = False
                        break
                if match:
                    amount = variant.get("amount", 0)
                    variant_id = variant.get("_id")
            while True:
                invoice_student_id = f"new_{StringUtil.generate_code('nnnnn')}"
                if invoice_student_id not in generated_ids:
                    generated_ids.append(invoice_student_id)
                    break

            item_ = {
                "_id": invoice_student_id,
                "student_id": i.get("_id"),
                "student_name": i.get("name"),
                "student_nis": i.get("nis"),
                "class_name": i.get("class_info").get("name"),
                "va_nos": i.get("va_nos"),
                "amount": amount,
                "variant_id": variant_id,
                "is_exists": False,
                "is_checked": False,
                "status": "waiting_for_payment",
            }
            if invoice_student_data.get(i.get("_id")):
                item_["is_exists"] = True
                item_["is_checked"] = True
                item_["amount"] = invoice_student_data.get(i.get("_id")).get("amount")
                item_["_id"] = invoice_student_data.get(i.get("_id")).get("_id")
                item_["status"] = invoice_student_data.get(i.get("_id")).get("status")
            data.append(item_)
        
        return {"data": data}

    
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        if _extra.get("school_class").get("school_id") != value.get("school_id"):
            raise ValidationError("Invalid school class")

        if _extra.get("finance_invoice_type").get("school_id") != value.get("school_id"):
            raise ValidationError("Invalid finance_invoice_type")

        student_ids = [ObjectId(item.get("student_id")) for item in value.get("student")]
        student_data = SchoolStudent().find({"_id": {"$in": student_ids}})
        for i in student_data:
            if i.get("school_id") != value.get("school_id") or i.get(
                "class_id"
            ) != value.get("class_id"):
                raise ValidationError("Invalid student")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        name = extra.get("finance_invoice_type").get("name")
        if extra.get("finance_invoice_type").get("type") == "year":
            name = f"{extra.get('finance_invoice_type').get('name')} TA. {extra.get('edu_academic_year').get('name')}"
        elif extra.get("finance_invoice_type").get("type") == "semester":
            name = f"{extra.get('finance_invoice_type').get('name')} Semester {validated_data.get('semester')} TA. {extra.get('edu_academic_year').get('name')}"
        elif extra.get("finance_invoice_type").get("type") == "month":
            name = f"{extra.get('finance_invoice_type').get('name')} Bulan {indonesian_months[validated_data.get('month') - 1]} TA. {extra.get('edu_academic_year').get('name')}"
        
        existing_ids = [
            ObjectId(item.get("_id"))
            for item in validated_data.get("student")
            if "new" not in item.get("_id")
        ]
        existing_invoices = model.find({"_id": {"$in": existing_ids}})
        existing_invoices = {item.get("_id"): item for item in existing_invoices}
        
        input_data = []
        update_data = []
        delete_ids = []
        update_student_data = []
        validated_data["student"] = [
            item for item in validated_data.get("student") if item.get("amount") > 0
        ]
        for i in validated_data.get("student"):
            if i.get("is_exists"):
                existing_invoice = existing_invoices.get(i.get("_id"))
                if existing_invoice.get("status") == "waiting_for_payment":
                    changes = i.get("amount") - existing_invoice.get(
                        "amount"
                    )
                    if i.get("is_checked"):
                        update_data.append(
                            {
                                "_id": ObjectId(i.get("_id")),
                                "set_data": {"amount": i.get("amount"),"rest": i.get("amount")},
                            }
                        )
                        if changes:
                            item_ = {
                                "_id": ObjectId(i.get("student_id")),
                                "inc_data": {"unpaid_total": changes},
                            }
                            update_student_data.append(item_)
                    else:
                        delete_ids.append(ObjectId(i.get("_id")))
                        item_ = {
                            "_id": ObjectId(i.get("student_id")),
                            "dec_data": {
                                "unpaid_total": existing_invoice.get(
                                    "amount"
                                )
                            },
                            "pull_data": {"unpaid_invoice_ids": [ObjectId(i.get("_id"))]},
                        }
                        update_student_data.append(item_)
            else:
                if i.get("is_checked"):                    
                    new_invoice_data = FinanceInvoiceData(
                        holding_id=ObjectId(extra.get("school_school").get("holding_id")) if extra.get("school_school").get("holding_id") else None,
                        school_id=ObjectId(validated_data.get("school_id")),
                        academic_year_id=ObjectId(validated_data.get("academic_year_id")),
                        semester=validated_data.get("semester"),
                        year=None,
                        month=validated_data.get("month"),
                        student_id=ObjectId(i.get("student_id")),
                        student_nis=i.get("student_nis"),
                        student_name=i.get("student_name"),
                        type_id=ObjectId(validated_data.get("type_id")),
                        type=extra.get("finance_invoice_type").get("type"),
                        is_installment=extra.get("finance_invoice_type").get("is_installment"),
                        name=name,
                        amount=i.get("amount"),
                        paid=0,
                        rest=i.get("amount"),
                        status="waiting_for_payment",
                        variant_id=ObjectId(validated_data.get("variant_id")),
                    )
                    input_data.append(new_invoice_data)
                    item_ = {
                        "_id": ObjectId(i.get("student_id")),
                        "inc_data": {"unpaid_total": i.get("amount")},
                        "add_to_set_data": {
                            "unpaid_invoice_ids": [new_invoice_data._id]
                        },
                    }
                    update_student_data.append(item_)

        if update_student_data:
            SchoolStudent().update_many_different_data(update_student_data)
        if input_data:
            SecurityValidator().validate_data(input_data)
            model.insert_many(input_data)
        if update_data:
            model.update_many_different_data(update_data)
        if delete_ids:
            model.delete({"_id": {"$in": delete_ids}})
            # model.soft_delete_many({"_id": {"$in": delete_ids}})
        return {
            "data": {},
            "message": None,
        }
