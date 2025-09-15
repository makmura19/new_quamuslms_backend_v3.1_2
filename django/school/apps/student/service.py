from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.school_student import SchoolStudent, SchoolStudentData
from models.school_school import SchoolSchool
from models.edu_academic_year import EduAcademicYear
from models.school_class import SchoolClass
from models.edu_stage_level import EduStageLevel
from models.edu_stage import EduStage
from bson import ObjectId
from datetime import datetime, timezone
from utils.datetime_util import DatetimeUtil


class MainService(BaseService):
    
    @staticmethod
    def create(model: SchoolStudent, validated_data, extra, user, headers_dict=None):
        holding_id = (
            ObjectId(extra.get("school_school").get("holding_id"))
            if extra.get("school_school").get("holding_id")
            else None
        )
        school_code = extra.get("school_school").get("code")
        academic_year_data = EduAcademicYear().get_active()
        academic_year_short = academic_year_data.get("name").replace("/", "")[2:]
        qrcode = model.get_qrcodes(
            school_code,
            academic_year_short,
            1
        )[0]
        degree_id = None
        level_id = ObjectId(extra.get("school_class").get("level_id")) if extra.get("school_class") else None
        if level_id:
            edu_level_data = EduStageLevel().find_one({"_id":level_id})
            if edu_level_data:
                degree_id = ObjectId(edu_level_data.get("degree_id"))
        
        new_student_data = SchoolStudentData(
            holding_id=holding_id,
            school_id=ObjectId(validated_data.get("school_id")),
            name=validated_data.get("name"),
            gender=validated_data.get("gender"),
            nis=validated_data.get("nis"),
            nisn=validated_data.get("nisn"),
            birth_date=validated_data.get("birth_date"),
            birth_place=validated_data.get("birth_place"),
            class_academic_year_id=extra.get("school_class").get("academic_year_id") if extra.get("school_class") else None,
            class_id=ObjectId(validated_data.get("class_id")) if validated_data.get("class_id") else None,
            degree_id=degree_id,
            stage_group_id=extra.get("school_school").get("stage_group_id"),
            stage_id=extra.get("school_school").get("stage_id"),
            level_id=level_id,
            level_seq=extra.get("school_class").get("level_sequence") if extra.get("school_class") else None,
            qrcode=qrcode,
            phone=validated_data.get("phone"),
            is_alumni=validated_data.get("is_alumni"),
            is_boarding=validated_data.get("is_boarding"),
            is_active=validated_data.get("is_active"),
        )
        SecurityValidator.validate_data(new_student_data)
        result = model.insert_one(new_student_data, user)
        if validated_data.get("class_id"):
            SchoolClass().update_one(
                {"_id":ObjectId(validated_data.get("class_id"))},
                add_to_set_data={"student_ids":[new_student_data._id]}
            )
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }
    

    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        update_student_data = {
            "name": validated_data.get("name"),
            "gender": validated_data.get("gender"),
            "nis": validated_data.get("nis") if validated_data.get("nis") else "",
            "nisn": validated_data.get("nisn") if validated_data.get("nisn") else "",
            "birth_place": validated_data.get("birth_place"),
            "birth_date": validated_data.get("birth_date"),
            "phone": validated_data.get("phone"),
            "is_alumni": validated_data.get("is_alumni"),
            "is_boarding": validated_data.get("is_boarding"),
            "is_active":validated_data.get("is_active"),
        }
        model.update_one({"_id":ObjectId(_id)},update_student_data, user=user)
        return {
            "data": {"id": str(_id)},
            "message": None,
        }


    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        from models.school_dormitory_room import SchoolDormitoryRoom
        from models.quran_class import QuranClass
        model.soft_delete({"_id": ObjectId(_id)}, old_data, user=user)
        if old_data.get("class_id"):
            SchoolClass().update_one(
                {"_id":ObjectId(old_data.get("class_id"))},
                pull_data={"student_ids":[ObjectId(_id)]},
                user=user
            )
        if old_data.get("dormitory_room_id"):
            SchoolDormitoryRoom().update_one(
                {"_id":ObjectId(old_data.get("dormitory_room_id"))},
                pull_data={"student_ids":[ObjectId(_id)]},
                user=user
            )
        if old_data.get("quran_class_ids"):
            quran_class_ids = [ObjectId(i) for i in old_data.get("quran_class_ids")]
            QuranClass().update_many(
                {"_id":{"$in":quran_class_ids}},
                pull_data={"student_ids":[ObjectId(_id)]}
                )
        return {}


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
            lookup=["school","user","class_academic_year","class","class_history","stage","level","quran_class"]
        )
        response_type = query_params.get("response_type")
        if response_type in ["xlsx"]:
            from helpers.openpyxl_helper import OpenpxlHelper

            export_data = [["No", "Kelas", "NIS", "NISN", "Nama", "Gender", "username", "password", "Kelas Tahfidz", "Kelas Tahsin", "Kelas Pra Tahsin"]]
            export_setting = [
                "w-5 text-center",
                "w-10 text-center",
                "w-20 text-center",
                "w-20 text-center",
                "w-40",
                "w-10 text-center",
                "w-15 text-center",
                "w-15 text-center",
                "w-25 text-center",
                "w-25 text-center",
                "w-25 text-center",
            ]


            for idx, item in enumerate(result["data"], start=1):
                tahfidz_class = []
                tahsin_class = []
                pra_tahsin_class = []
                if item.get("quran_class_ids"):
                    for quran_class in item.get("quran_class_info"):
                        if quran_class.get("program_type") ==  "tahfidz":
                            tahfidz_class.append(quran_class.get("name"))
                        if quran_class.get("program_type") ==  "tahsin":
                            tahsin_class.append(quran_class.get("name"))
                        if quran_class.get("program_type") ==  "pra_tahsin":
                            pra_tahsin_class.append(quran_class.get("name"))
                export_data.append(
                    [
                        idx,
                        item.get("class_info").get("name") if item.get("class_info") else "",
                        item.get("nis", ""),
                        item.get("nisn", ""),
                        item.get("name", ""),
                        "L" if item.get("gender") == "male" else "P",
                        (
                            item.get("user_info").get("login").split("_")[1]
                            if item.get("user_id")
                            else "-"
                        ),
                        (
                            item.get("user_info").get("password")
                            if item.get("user_id")
                            else "-"
                        ),
                        ", ".join(tahfidz_class) if tahfidz_class else "",
                        ", ".join(tahsin_class) if tahsin_class else "",
                        ", ".join(pra_tahsin_class) if pra_tahsin_class else "",
                    ]
                )

            export_kwargs = {
                "data": export_data,
                "setting": export_setting,
                "filename": "student",
                "title": "Data Siswa",
            }

            helper_class = {
                "xlsx": OpenpxlHelper,
            }.get(response_type)

            return helper_class(**export_kwargs).response
        return result
    

    @staticmethod
    def upload_photo(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from utils.file_storage_util import FileStorageUtil
        
        url = FileStorageUtil.upload_aws(
            validated_data.get("file"),
            f"{str(old_data.get('school_id'))}/student_book/{str(_id)}/file1",
        )
        if not url:
            raise ValidationError("Failed to upload photo.")
        update_data = {"photo": url[0]}
        model.update_one({"_id": ObjectId(_id)}, update_data, user=user)
        return {
            "data": {"id": str(_id)},
            "message": None,
        }
    

    @staticmethod
    def input_xls(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from utils.excel_util import ExcelUtils

        schema = {
            "KELAS": {"type": "string", "required": False},
            "NIS": {"type": "string", "required": False},
            "NISN": {"type": "string", "required": False},
            "NAMA": {"type": "string", "required": True},
            "GENDER": {"type": "enum", "choices": ["L", "P"], "required": True},
            "NO ORANGTUA": {"type": "phone", "required": False},
        }
        excel_data = ExcelUtils.read(validated_data.get("file"), schema=schema)
        
        if excel_data == None:
            raise ValidationError("Invalid input data")

        now = datetime.now(timezone.utc)
        academic_year_data = EduAcademicYear().find_one({
            "start_date": { "$lte": now },
            "end_date": { "$gte": now }
        })
        academic_year_short = academic_year_data.get("name").replace("/", "")[2:]
        school_data = extra.get("school_school")
        holding_id = (
            ObjectId(school_data.get("holding_id"))
            if school_data.get("holding_id")
            else None
        )
        qrcode = model.get_qrcodes(
            school_data.get("code"),
            academic_year_short,
            len(excel_data)
        )
        school_class_data = SchoolClass().find({
            "school_id":ObjectId(validated_data.get("school_id")),
            "academic_year_id":ObjectId(academic_year_data.get("_id"))
        })
        school_class_map = {
            i.get("name").lower(): {
                "_id": ObjectId(i.get("_id")),
                "class_academic_year_id": ObjectId(i.get("academic_year_id")),
                "level_id": ObjectId(i.get("level_id")),
                "level_seq": i.get("level_sequence"),
            }
            for i in school_class_data
        }
        
        input_data = []
        push_data_map = {}
        level_degree_map = {}
        for idx, i in enumerate(excel_data):
            student_id = ObjectId()
            class_info = {}
            if i.get("KELAS"):
                if i.get("KELAS").lower() in school_class_map.keys():
                    class_info.update(school_class_map.get(i.get("KELAS").lower()))
                    class_id = class_info.get("_id")
                    if class_id not in push_data_map.keys():
                        push_data_map.update({class_id:[]})
                    push_data_map[class_id].append(student_id)
                else:
                    raise ValidationError(f"Failed to input data. Class '{i.get('KELAS')}' does not exist.")
            
            
            level_id = class_info.get("level_id")
            if level_id:
                if level_id not in level_degree_map.keys():
                    edu_level_data = EduStageLevel().find_one({"_id":level_id})
                    if edu_level_data:
                        level_degree_map.update({level_id:edu_level_data.get("degree_id")})


            new_student_data = SchoolStudentData(
                _id=student_id,
                holding_id=holding_id,
                school_id=ObjectId(validated_data.get("school_id")),
                name=i.get("NAMA"),
                gender="male" if i.get("GENDER") == "L" else "female",
                nis=i.get("NIS") if i.get("NIS") else "",
                nisn=i.get("NISN") if i.get("NISN") else "",
                class_academic_year_id=class_info.get("class_academic_year_id"),
                class_id=class_info.get("_id"),
                degree_id=level_degree_map.get("degree_id"),
                stage_group_id=school_data.get("stage_group_id"),
                stage_id=school_data.get("stage_id"),
                level_id=class_info.get("level_id"),
                level_seq=class_info.get("level_seq"),
                qrcode=qrcode[idx],
                phone=i.get("NO ORANGTUA"),
                is_alumni=False,
                is_boarding=False,
                is_active=True,
            )
            input_data.append(new_student_data)
        SecurityValidator.validate_data(input_data)

        if input_data:
            model.insert_many(input_data)
        if push_data_map:
            push_data = [
                {
                    "_id": k,
                    "add_to_set_data": {"student_ids":v}
                }
                for k,v in push_data_map.items()
            ]
            SchoolClass().update_many_different_data(push_data)            
        return {
            "message": None,
        }


    @staticmethod
    def export_update(
        model: BaseModel, query_params, params_validation, user, headers_dict=None
    ):
        from helpers.openpyxl_helper import OpenpxlHelper
        result = model.aggregate(
            add_metadata=True,
            query_params=query_params,
            params_validation=params_validation,
            fields=query_params.get("fields"),
            exclude=query_params.get("exclude"),
        )
        join_map = {}
        export_data = [["No", "ID", "NIS", "NISN", "Nama", "Gender", "Tahun Masuk", "Tempat Lahir", "Tanggal Lahir", "No. Orang Tua", "Alumni", "Boarding"]]
        export_setting = ["w-5 text-center", "w-30", "w-17 text-center", "w-17 text-center", "w-35", "w-10 text-center", "w-18 text-center", "w-18 text-center", "w-18 text-center", "w-20 text-center", "w-10 text-center", "w-10 text-center"]
        join_map = {}        
        for idx, item in enumerate(result.get("data"), start=1):
            join_id = item.get("join_academic_year_id")
            if join_id:
                if join_id not in join_map.keys():
                    join_year_data = EduAcademicYear().find_one({"_id":join_id})
                    join_map.update({join_id:join_year_data.get("year")})
            birth_date = DatetimeUtil.from_string(item.get("birth_date")) if item.get("birth_date") else None
            birth_date = DatetimeUtil.to_string(birth_date, "%d-%m-%Y") if birth_date else None
            export_data.append([
                idx,
                item.get("_id", ""),
                item.get("nis", ""),
                item.get("nisn", ""),
                item.get("name", ""),
                "L" if item.get("gender") == "male" else "P",
                join_map.get(join_id) if join_id else "",
                item.get("birth_place", ""),
                birth_date,
                item.get("phone", ""),
                "Ya" if item.get("is_alumni") else "Tidak",
                "Ya" if item.get("is_boarding") else "Tidak"
            ])
        
        export_kwargs = {
            "data": export_data,
            "setting": export_setting,
            "filename": "data_siswa",
        }
        helper_class = {
            "xlsx": OpenpxlHelper,
        }.get("xlsx")

        return helper_class(**export_kwargs).response



    @staticmethod
    def import_update(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from utils.excel_util import ExcelUtils

        schema = {
            "ID": {"type": "string", "required": True},
            "NIS": {"type": "string", "required": False},
            "NISN": {"type": "string", "required": False},
            "Nama": {"type": "string", "required": True},
            "Gender": {"type": "enum", "choices": ["L", "P"], "required": True},
            "Tahun Masuk": {"type": "int", "required": False},
            "Tempat Lahir": {"type": "string", "required": False},
            "Tanggal Lahir": {"type": "date", "required": False},
            "No. Orang Tua": {"type": "phone", "required": False},
            "Alumni": {"type": "enum", "choices": ["Ya", "Tidak"], "required": False},
            "Boarding": {"type": "enum", "choices": ["Ya", "Tidak"], "required": False},
        }

        excel_data = ExcelUtils.read(validated_data.get("file"), schema=schema)
        
        if excel_data == None:
            raise ValidationError("Invalid input data")
        
        join_data = EduAcademicYear().find()
        join_map = {i.get("year"):ObjectId(i.get("_id")) for i in join_data}
        update_student_data = {}

        for idx, item in enumerate(excel_data):
            student_id = ObjectId(item.get("ID"))
            if item.get("Tahun Masuk") and item.get("Tahun Masuk") not in join_map.keys():
                raise ValidationError(f"Invalid 'Tahun Masuk'. There is no {item.get('Tahun Masuk')} in the edu_academic_year database yet.")

            birth_date = None
            if item.get("Tanggal Lahir"):
                birth_date = item.get("Tanggal Lahir").strftime("%Y-%m-%d")
                birth_date = DatetimeUtil.from_string(birth_date)
            student_data = {
                "nis": item.get("NIS") if item.get("NIS") else "",
                "nisn": item.get("NISN") if item.get("NISN") else "",
                "name": item.get("Nama"),
                "gender": "male" if item.get("Gender") == "L" else "female",
                "join_academic_year_id": join_map.get(item.get("Tahun Masuk")),
                "birth_place": item.get("Tempat Lahir") if item.get("Tempat Lahir") else None,
                "birth_date": birth_date,
                "phone": item.get("No. Orang Tua") if item.get("No. Orang Tua") else None,
                "is_alumni": True if item.get("Alumni") else False,
                "is_boarding": True if item.get("Boarding") else False,
            }
            update_student_data.update({student_id:student_data})

        update_student_data = [
            {
                "_id": k,
                "set_data": v,
            } 
            for k,v in update_student_data.items()
        ]
        
        SchoolStudent().update_many_different_data(update_student_data)
        return {
            "message": None,
        }


    @staticmethod
    def account(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        MainService.make_account(_id, old_data, user)
        return {
            "data": {"id": str(_id)},
            "message": None,
        }
    
    @staticmethod
    def make_account(_id, old_student_data, user):
        from models.school_school import SchoolSchool
        from models.res_user import ResUser, ResUserData
        from models.res_authority import ResAuthority
        from models.authentication_user import AuthenticationUserData
        from constants.access import Role
        from helpers.user_service import UserService
        from models.school_student import SchoolStudent

        if old_student_data.get("user_id"):
            raise ValidationError("Invalid student_id, account already exists")
        school_data = SchoolSchool().find_one({"_id":old_student_data.get("school_id")})
        username = ResUser().get_school_username(
            old_student_data.get("school_id"),
            school_data.get("code"),
            old_student_data.get("name")
        )
        authority_data = ResAuthority().find_one({"code": Role.STUDENT})
        new_user_data = ResUserData(
            holding_id=ObjectId(old_student_data.get("holding_id")) if old_student_data.get("holding_id") else None,
            school_id=ObjectId(old_student_data.get("school_id")),
            student_id=ObjectId(_id),
            login=username,
            name=old_student_data.get("name"),
            authority_id=ObjectId(authority_data.get("_id")),
            authority_ids=[ObjectId(authority_data.get("_id"))],
            authority_codes=[authority_data.get("code")],
            is_password_encrypted=False,
            is_student=True,
            is_active=True,
        )
        new_auth_data = AuthenticationUserData(
            school_id=str(old_student_data.get("school_id")),
            holding_id=str(old_student_data.get("holding_id")) if old_student_data.get("holding_id") else "",
            school_code=school_data.get("code"),
            username=new_user_data.login,
            password=new_user_data.password,
            role=",".join(new_user_data.authority_codes),
            is_staff=False,
            is_active=True,
            is_company_active=True,
        )
        SecurityValidator.validate_data(new_user_data, new_auth_data)
        ResUser().insert_one(new_user_data, user=user)
        UserService.create_user(new_auth_data)
        SchoolStudent().update_one(
            {"_id":ObjectId(_id)},
            {
                "user_id":new_user_data._id,
                "login":new_user_data.login
            }
        )
        return new_user_data._id, new_user_data.login


    @staticmethod
    def activate(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from models.res_user import ResUser
        from helpers.user_service import UserService

        _id = ObjectId(_id)
        if old_data.get("is_active") == validated_data.get("is_active"):
            raise ValidationError("Invalid student_id. Student data is already active or already inactive.")

        update_student_data = {"is_active": validated_data.get("is_active")}
        res_user_data = ResUser().find_one({"student_id": _id})
        user_id = ObjectId(res_user_data.get("_id")) if res_user_data else None
        login = res_user_data.get("login") if res_user_data else None
        if validated_data.get("is_active"):
            if res_user_data:
                update_student_data.update({
                    "user_id":user_id,
                    "login":login
                })
            else:
                user_id, login = MainService.make_account(_id, old_data, user)
                update_student_data.update({
                    "user_id":user_id,
                    "login":login
                })
        else:
            update_student_data.update({
                "user_id":None,
                "login":None
            })
        
        model.update_one(
            {"_id": _id},
            update_student_data,
        )
        if res_user_data:
            ResUser().update_one({"_id": user_id}, {"is_active":validated_data.get("is_active")})
            UserService().update_user_is_active(login, validated_data.get("is_active"))
        return {
            "data": {"id": str(_id)},
            "message": None,
        }
    

    @staticmethod
    def validate_update_pin(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        if len(value.get("pin")) != 5:
            raise ValidationError("PIN must consist of 5 digits.")
        if value.get("pin") == old_data.get("pin"):
            raise ValidationError("PIN does not change.")
        if not value.get("pin").isnumeric():
            raise ValidationError("PIN must consist of numbers only.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}


    # @staticmethod
    # def validate_update_pin(value, _extra, secret, user, old_data=None):
    #     from utils.dict_util import DictUtil
    #     if value.get("old_pin") != old_data.get("pin"):
    #         raise ValidationError("Old PIN is wrong.")
    #     if value.get("old_pin") == value.get("new_pin_1"):
    #         raise ValidationError("PIN does not change.")
    #     if value.get("new_pin_1") == value.get("new_pin_2"):
    #         raise ValidationError("Confirm PIN does not match.")
    #     for k,v in value.items():
    #         if len(v) != 5:
    #             raise ValidationError(f"{'Old' if k == 'old_pin' else 'New'} PIN must consist of 5 digits.")
    #         if not v.isnumeric():
    #             raise ValidationError(f"{'Old' if k == 'old_pin' else 'New'} PIN must consist of numbers only.")
    #     extra = {}
    #     return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}


    @staticmethod
    def update_pin(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        model.update_one({"_id":ObjectId(_id)},{"pin":validated_data.get("pin")})
        return {
            "data": {"id": str(_id)},
            "message": None,
        }


    @staticmethod
    def validate_move_class(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        if old_data.get("class_id") == ObjectId(value.get("class_id")):
            raise ValidationError("Class does not change.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}
    

    @staticmethod
    def move_class(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        _id = ObjectId(_id)
        old_class_id = old_data.get("class_id")
        new_class_id = ObjectId(validated_data.get("class_id")) if validated_data.get("class_id") else None
        new_class_data = SchoolClass().find_one({"_id":new_class_id})
        level_id = new_class_data.get("level_id") if new_class_data else None
        degree_id = None
        if level_id:
            edu_level_data = EduStageLevel().find_one({"_id":level_id})
            if edu_level_data:
                degree_id = ObjectId(edu_level_data.get("degree_id"))
        if old_class_id:
            SchoolClass().update_one({"_id":old_class_id},pull_data={"student_ids":[_id]})
        if new_class_id:
            SchoolClass().update_one({"_id":new_class_id},add_to_set_data={"student_ids":[_id]})
        model.update_one(
            {"_id":_id},
            {
                "class_id": new_class_id,
                "level_id": level_id,
                "level_seq": new_class_data.get("level_sequence") if new_class_data else None,
                "degree_id": degree_id,
                "class_academic_year_id": new_class_data.get("academic_year_id") if new_class_data else None,
            }
        )
        return {
            "data": {"id": str(_id)},
            "message": None,
        }


    @staticmethod
    def validate_class_(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        print(old_data.get("class_id"))
        if old_data.get("class_id"):
            raise ValidationError("Student already have class.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}
    

    @staticmethod
    def class_(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        _id = ObjectId(_id)
        new_class_id = ObjectId(validated_data.get("class_id"))
        new_class_data = SchoolClass().find_one({"_id":new_class_id})
        level_id = new_class_data.get("level_id") if new_class_data else None
        degree_id = None
        if level_id:
            edu_level_data = EduStageLevel().find_one({"_id":level_id})
            if edu_level_data:
                degree_id = ObjectId(edu_level_data.get("degree_id"))
        if new_class_id:
            SchoolClass().update_one({"_id":new_class_id},add_to_set_data={"student_ids":[_id]})
        model.update_one(
            {"_id":_id},
            {
                "class_id": new_class_id,
                "level_id": level_id,
                "level_seq": new_class_data.get("level_sequence") if new_class_data else None,
                "degree_id": degree_id,
                "class_academic_year_id": new_class_data.get("academic_year_id") if new_class_data else None,
            }
        )
        return {
            "data": {"id": str(_id)},
            "message": None,
        }