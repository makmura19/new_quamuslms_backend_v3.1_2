from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.edu_academic_year import EduAcademicYearData, EduAcademicYear
from models.edu_semester import EduSemester, EduSemesterData
from bson import ObjectId
import json
from datetime import datetime


class MainService(BaseService):
    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        fields = MainService.create__fields(validated_data.get("year"))

        new_ay_data = EduAcademicYearData(
            name=fields["name"],
            short_name=fields["short_name"],
            year=validated_data["year"],
            start_date=datetime.strptime(fields["start_date"], "%Y-%m-%d"),
            end_date=datetime.strptime(fields["end_date"], "%Y-%m-%d"),
            semester_ids=fields["semester_ids"],
        )

        semester_doc = [
            EduSemesterData(
                _id=i,
                academic_year_id=new_ay_data._id,
                semester_no=idx + 1,
                name="Ganjil" if idx + 1 == 1 else "Genap",
                start_date=MainService.create__semester_range(
                    validated_data.get("year"), idx + 1
                ).get("start_date"),
                end_date=MainService.create__semester_range(
                    validated_data.get("year"), idx + 1
                ).get("end_date"),
            )
            for idx, i in enumerate(fields["semester_ids"])
        ]

        SecurityValidator.validate_data(new_ay_data, semester_doc)

        result = model.insert_one(new_ay_data)
        if semester_doc:
            EduSemester().insert_many(semester_doc)

        return {
            "data": {"_id": str(result.inserted_id)},
            "message": "Data berhasil dibuat.",
        }

    @staticmethod
    def create__fields(year):
        name = f"{int(year)}/{int(year)+1}"
        short_name = f"{str(year)[-2:]}{str(int(year)+1)[-2:]}"
        start_date = f"{int(year)}-07-01"
        end_date = f"{int(year)+1}-06-30"
        semester_ids = [ObjectId(), ObjectId()]

        return {
            "name": name,
            "short_name": short_name,
            "start_date": start_date,
            "end_date": end_date,
            "semester_ids": semester_ids,
        }

    @staticmethod
    def create__semester_range(year, semester_number):
        if semester_number == 1:
            start_date = datetime.strptime(f"{year}-07-01", "%Y-%m-%d")
            end_date = datetime.strptime(f"{year}-12-31", "%Y-%m-%d")
        else:
            start_date = datetime.strptime(f"{year+1}-01-01", "%Y-%m-%d")
            end_date = datetime.strptime(f"{year+1}-06-30", "%Y-%m-%d")

        return {"start_date": start_date, "end_date": end_date}

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
            lookup=["semester"],
        )
        return result

    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        existing_id = model.find_one({"_id": ObjectId(_id)})
        existing_year = model.find_one({"year": validated_data.get("year")})
        if existing_year:
            if existing_year.get("_id") != _id:
                raise ValidationError(
                    f"Data tahun akademik {validated_data.get('year')}/{validated_data.get('year')+1} sudah ada."
                )
            else:
                pass

        fields = MainService.create__fields(validated_data.get("year"))
        fields["semester_ids"] = existing_id["semester_ids"]

        update_data = {
            "name": fields.get("name"),
            "short_name": fields.get("short_name"),
            "start_date": datetime.strptime(fields.get("start_date"), "%Y-%m-%d"),
            "end_date": datetime.strptime(fields.get("end_date"), "%Y-%m-%d"),
        }
        semester_update = [
            {
                "_id": i,
                "set_data": {
                    "start_date": MainService.create__semester_range(
                        validated_data.get("year"), idx + 1
                    ).get("start_date"),
                    "end_date": MainService.create__semester_range(
                        validated_data.get("year"), idx + 1
                    ).get("end_date"),
                },
            }
            for idx, i in enumerate(fields["semester_ids"])
        ]

        model.update_one({"_id": ObjectId(_id)}, update_data=update_data, user=user)
        EduSemester().update_many_different_data(semester_update)

        return {
            "data": {"id": _id},
            "message": None,
        }

    @staticmethod
    def destroy(model, _id, old_data, user, headers_dict=None):
        EduSemester().soft_delete_many({"academic_year_id": ObjectId(_id)})

        model.soft_delete({"_id": ObjectId(_id)}, old_data, user=user)

        return {}
