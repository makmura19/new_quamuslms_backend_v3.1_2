from constants.module import ModuleEnum
from bson import ObjectId
from models.school_school import SchoolSchool
from models.edu_stage_group import EduStageGroup


class Module:

    def __init__(self, _id, old_data, validated_data, extra, user):
        self._id = _id
        self.old_data = old_data
        self.validated_data = validated_data
        self.extra = extra
        self.user = user
        self.module_codes = [
            item.get("code") for item in self.extra.get("school_module")
        ]

        self.stage_group_data = EduStageGroup().find_one(
            {"_id": ObjectId(self.old_data.get("stage_group_id"))}
        )

        self.level_ids = [
            ObjectId(item) for item in self.stage_group_data.get("level_ids")
        ]

        if ModuleEnum.LMS.value in self.module_codes and not self.old_data.get(
            "config_lms_id"
        ):
            self.register_lms()

        if ModuleEnum.ATTENDANCE.value in self.module_codes and not self.old_data.get(
            "is_attendace_created"
        ):
            self.register_attendance()

        if ModuleEnum.TAHFIDZ.value in self.module_codes and not self.old_data.get(
            "config_tahfidz_id"
        ):
            self.register_quran("tahfidz")

        if ModuleEnum.TAHSIN.value in self.module_codes and not self.old_data.get(
            "config_tahsin_id"
        ):
            self.register_quran("tahsin")

        if ModuleEnum.PRA_TAHSIN.value in self.module_codes and not self.old_data.get(
            "config_pratahsin_id"
        ):
            self.register_quran("pra_tahsin")

        if ModuleEnum.MUTABAAH.value in self.module_codes and not self.old_data.get(
            "config_mutabaah_id"
        ):
            self.register_mutabaah()

        if ModuleEnum.FINANCE.value in self.module_codes and not self.old_data.get(
            "config_finance_id"
        ):
            self.register_finance()

        SchoolSchool().update_one(
            {"_id": ObjectId(self._id)},
            {
                "module_ids": [
                    ObjectId(item) for item in validated_data.get("module_ids")
                ],
                "module_codes": self.module_codes,
            },
        )

    def register_lms(self):
        from models.config_lms import ConfigLms, ConfigLmsData
        from models.school_school import SchoolSchool

        exam_type_ids = self.create_lms_exam_type()
        config_report_id = self.create_config_lms_report()

        new_config_lms_data = ConfigLmsData(
            school_id=ObjectId(self._id),
            exam_type_ids=exam_type_ids,
            config_report_id=config_report_id,
            num_option=self.stage_group_data.get("num_option"),
        )
        ConfigLms().insert_one(new_config_lms_data)

        self.create_subject()
        SchoolSchool().update_one(
            {"_id": ObjectId(self._id)},
            {"config_lms_id": new_config_lms_data._id, "is_subject_created": True},
        )

    def create_lms_exam_type(self):
        from models.lms_exam_type import LmsExamType, LmsExamTypeData

        tf_data = LmsExamTypeData(
            school_id=ObjectId(self._id),
            code="tf",
            name="Tes Formatif",
            weight=1,
            is_template=True,
            is_report=True,
            is_final=False,
            is_odd_semester=True,
            is_even_semester=True,
        )
        ts_data = LmsExamTypeData(
            school_id=ObjectId(self._id),
            code="ts",
            name="Tes Sumatif",
            weight=1,
            is_template=True,
            is_report=True,
            is_final=False,
            is_odd_semester=True,
            is_even_semester=True,
        )
        asts_data = LmsExamTypeData(
            school_id=ObjectId(self._id),
            code="asts",
            name="Asesmen Sumatif Tengah Semester",
            weight=1,
            is_template=True,
            is_report=True,
            is_final=False,
            is_odd_semester=True,
            is_even_semester=True,
        )
        asas_data = LmsExamTypeData(
            school_id=ObjectId(self._id),
            code="asas",
            name="Asesmen Sumatif Akhir Semester",
            weight=1,
            is_template=True,
            is_report=True,
            is_final=True,
            is_odd_semester=True,
            is_even_semester=False,
        )
        asat_data = LmsExamTypeData(
            school_id=ObjectId(self._id),
            code="asat",
            name="Asesmen Sumatif Akhir Tahun",
            weight=1,
            is_template=True,
            is_report=True,
            is_final=True,
            is_odd_semester=False,
            is_even_semester=True,
        )
        LmsExamType().insert_many([tf_data, ts_data, asts_data, asas_data, asat_data])
        return [tf_data._id, ts_data._id, asts_data._id, asas_data._id, asat_data._id]

    def create_config_lms_report(self):
        from models.config_lms_report import ConfigLmsReport, ConfigLmsReportData
        from models.lms_report_type import LmsReportType

        report_type_data = LmsReportType().find_one({"code": "REP-01"})

        new_data = ConfigLmsReportData(
            school_id=ObjectId(self._id),
            type_id=ObjectId(report_type_data.get("_id")),
            student_info={
                "academic_class": True,
                "quran_class": True,
                "teacher": True,
                "semester": True,
                "academic_year": True,
                "nis": True,
                "nisn": True,
                "order": [
                    "academic_class",
                    "quran_class",
                    "teacher",
                    "semester",
                    "academic_year",
                    "nis",
                    "nisn",
                ],
            },
            header={
                "school_logo": True,
                "quamus_logo": False,
                "holding_logo": False,
                "address": True,
                "title": True,
                "periodic_title": True,
                "academic_year": True,
                "order": [
                    "school_logo",
                    "address",
                    "title",
                    "periodic_title",
                    "academic_year",
                ],
            },
            signature={
                "principal": True,
                "coordinator": True,
                "parent": True,
                "quamus": False,
            },
            report_rubric=[
                {"letter": "D", "name": "Kurang", "gte": 0, "lte": 60},
                {"letter": "C", "name": "Cukup", "gte": 61, "lte": 75},
                {"letter": "B", "name": "Baik", "gte": 76, "lte": 90},
                {"letter": "A", "name": "Amat Baik", "gte": 91, "lte": 100},
            ],
        )
        ConfigLmsReport().insert_one(new_data)
        return new_data._id

    def create_subject(self):
        from models.edu_subject import EduSubject
        from models.edu_subject_level import EduSubjectLevel, EduSubjectLevelData
        from models.edu_stage_level import EduStageLevel
        from models.school_subject import SchoolSubject, SchoolSubjectData

        subject_level_data = EduSubjectLevel().find(
            {"level_id": {"$in": self.level_ids}}
        )
        grouped = {}
        for i in subject_level_data:
            grouped.setdefault(i.get("subject_id"), [])
            grouped[i.get("subject_id")].append(i.get("level_id"))

        subject_ids = [ObjectId(k) for k, v in grouped.items()]
        subject_data = EduSubject().find({"_id": {"$in": subject_ids}})
        subject_data = {item.get("_id"): item for item in subject_data}

        input_data = []
        for k, v in grouped.items():
            selected_subject = subject_data.get(k)
            new_school_subject_data = SchoolSubjectData(
                school_id=ObjectId(self._id),
                subject_id=ObjectId(k),
                name=selected_subject.get("name"),
                short_name=selected_subject.get("short_name"),
                threshold=70,
                sequence=selected_subject.get("sequence"),
                level_ids=[ObjectId(item) for item in v],
                is_template=True,
                is_active=True,
            )
            input_data.append(new_school_subject_data)
        if input_data:
            SchoolSubject().insert_many(input_data)

    def register_attendance(self):
        from models.tap_attendance_group import (
            TapAttendanceGroup,
            TapAttendanceGroupData,
        )

        group_id, schedule_ids = self.create_student_schedule()

        new_tap_attendance_group_data = TapAttendanceGroupData(
            _id=group_id,
            school_id=ObjectId(self._id),
            name="Jadwal Reguler Siswa",
            for_student=True,
            for_teacher=False,
            teacher_ids=[],
            schedule_ids=schedule_ids,
            is_all_teacher=False,
            is_default=True,
            is_active=True,
        )
        TapAttendanceGroup().insert_one(new_tap_attendance_group_data)

        group_id, schedule_ids = self.create_teacher_schedule()

        new_tap_attendance_group_data = TapAttendanceGroupData(
            _id=group_id,
            school_id=ObjectId(self._id),
            name="Jadwal Reguler Guru",
            for_student=False,
            for_teacher=True,
            teacher_ids=[],
            schedule_ids=schedule_ids,
            is_all_teacher=True,
            is_default=True,
            is_active=True,
        )
        TapAttendanceGroup().insert_one(new_tap_attendance_group_data)

        SchoolSchool().update_one(
            {"_id": ObjectId(self._id)}, {"is_attendace_created": True}
        )

    def create_student_schedule(self):

        from models.tap_attendance_schedule import (
            TapAttendanceSchedule,
            TapAttendanceScheduleData,
        )

        days = ["mon", "tue", "wed", "thu", "fri"]

        group_id = ObjectId()

        input_data = []
        for i in days:
            for j in self.level_ids:
                new_tap_attendance_schedule_data = TapAttendanceScheduleData(
                    school_id=ObjectId(self._id),
                    group_id=group_id,
                    level_id=ObjectId(j),
                    day=i,
                    check_in_time=7.0,
                    check_out_time=14.0,
                    late_after=7.0,
                    early_leave_before=14.0,
                    for_student=True,
                    for_teacher=False,
                    is_active=True,
                )
                input_data.append(new_tap_attendance_schedule_data)

        if input_data:
            TapAttendanceSchedule().insert_many(input_data)

        return group_id, [item._id for item in input_data]

    def create_teacher_schedule(self):

        from models.tap_attendance_schedule import (
            TapAttendanceSchedule,
            TapAttendanceScheduleData,
        )

        days = ["mon", "tue", "wed", "thu", "fri"]

        group_id = ObjectId()

        input_data = []
        for i in days:
            new_tap_attendance_schedule_data = TapAttendanceScheduleData(
                school_id=ObjectId(self._id),
                group_id=group_id,
                level_id=None,
                day=i,
                check_in_time=7.0,
                check_out_time=14.0,
                late_after=7.0,
                early_leave_before=14.0,
                for_student=False,
                for_teacher=True,
                is_active=True,
            )
            input_data.append(new_tap_attendance_schedule_data)

        if input_data:
            TapAttendanceSchedule().insert_many(input_data)

        return group_id, [item._id for item in input_data]

    def register_quran(self, program_type):
        from models.quran_report_type import QuranReportType
        from models.config_quran import ConfigQuran, ConfigQuranData
        from models.config_quran_report import ConfigQuranReport, ConfigQuranReportData

        report_type_code = {
            "tahfidz": "REP-TF-01",
            "tahsin": "REP-TH-01",
            "pra_tahsin": "REP-PT-01",
        }
        report_type_data = QuranReportType().find_one(
            {"code": report_type_code.get(program_type)}
        )

        report_config_id = ObjectId()
        new_config_quran_data = ConfigQuranData(
            school_id=ObjectId(self._id),
            report_config_id=report_config_id,
            daily_assesment_rule="type_1",
            exam_assesment_rule="type_1",
            juziyah_assesment_rule="type_1",
            coordinator_id=None,
            teacher_ids=[],
            target_period="year",
            exam_threshold=None,
            use_matrix=False,
            multiple_class_per_student=False,
            program_type=program_type,
            use_whatsapp=False,
            whatsapp_no=None,
            quran_type="kemenag",
            is_active=True,
        )
        new_config_quran_report_data = ConfigQuranReportData(
            _id=report_config_id,
            school_id=ObjectId(self._id),
            student_info={
                "academic_class": True,
                "quran_class": True,
                "teacher": True,
                "semester": True,
                "academic_year": True,
                "nis": True,
                "nisn": True,
                "order": [
                    "academic_class",
                    "quran_class",
                    "teacher",
                    "semester",
                    "academic_year",
                    "nis",
                    "nisn",
                ],
            },
            header={
                "school_logo": True,
                "quamus_logo": False,
                "holding_logo": False,
                "address": True,
                "title": True,
                "periodic_title": True,
                "academic_year": True,
                "order": [
                    "school_logo",
                    "address",
                    "title",
                    "periodic_title",
                    "academic_year",
                ],
            },
            signature={
                "principal": True,
                "coordinator": True,
                "parent": True,
                "quamus": False,
            },
            label={
                "principal": "Kepala Sekolah",
                "coordinator": "Koordinator",
                "parent": "Wali Murid",
                "title": "Laporan",
                "periodic_title": "",
                "place": "",
                "address": "",
            },
            use_chapter_recap=False,
            total_rule="average",
            component_score={"is_daily": True, "is_exam": True},
            report_rubric=[
                {"letter": "D", "name": "Kurang", "gte": 0, "lte": 60},
                {"letter": "C", "name": "Cukup", "gte": 61, "lte": 75},
                {"letter": "B", "name": "Baik", "gte": 76, "lte": 90},
                {"letter": "A", "name": "Amat Baik", "gte": 91, "lte": 100},
            ],
            type_id=ObjectId(report_type_data.get("_id")),
        )
        ConfigQuran().insert_one(new_config_quran_data)
        ConfigQuranReport().insert_one(new_config_quran_report_data)
        SchoolSchool().update_one(
            {"_id": ObjectId(self._id)},
            {f"config_{program_type.replace('_','')}_id": new_config_quran_data._id},
        )

    def register_mutabaah(self):
        from models.config_mutabaah import ConfigMutabaah, ConfigMutabaahData

        new_config_mutabaah_data = ConfigMutabaahData(
            school_id=ObjectId(self._id),
            use_group=False,
            use_class=False,
            score_format="letter",
        )
        ConfigMutabaah().insert_one(new_config_mutabaah_data)
        SchoolSchool().update_one(
            {"_id": ObjectId(self._id)},
            {"config_mutabaah_id": new_config_mutabaah_data._id},
        )

    def register_finance(self):
        from models.account_account import AccountAccount, AccountAccountData
        from models.config_finance import ConfigFinance, ConfigFinanceData

        self.create_account()
        cash_id = AccountAccount().create_school_account(
            self._id, "1100", f"Kas Utama {self.old_data.get('name').upper()}"
        )
        payable_id = AccountAccount().create_school_account(
            self._id, "2100", f"Utang Quamus {self.old_data.get('name').upper()}"
        )

        new_config_finance_data = ConfigFinanceData(
            holding_id=None,
            school_id=ObjectId(self._id),
            payable_id=payable_id,
            cash_id=cash_id,
            sharing_percentage=0,
            daily_pocket_treshold=10000,
            company_fee=2000,
            prefix="01",
            is_auto_debit=False,
            is_pocket_auto_debit=False,
            va_config_ids=[],
            receipt={"header": "", "place": ""},
            merchant_ids=[],
            is_prefix_lock=False,
            is_active=True,
        )
        ConfigFinance().insert_one(new_config_finance_data)
        SchoolSchool().update_one(
            {"_id": ObjectId(self._id)},
            {
                "config_finance_id": new_config_finance_data._id,
                "is_account_created": True,
                "payable_id": payable_id,
                "cash_id": cash_id,
            },
        )

    def create_account(self):
        from models.account_account import AccountAccount, AccountAccountData

        account_data = AccountAccount().find({"is_template": True})

        input_data = []
        for i in account_data:
            new_account_account_data = AccountAccountData(
                holding_id=None,
                school_id=ObjectId(self._id),
                code=i.get("code"),
                name=i.get("name"),
                type=i.get("type"),
                group=i.get("group"),
                parent_id=i.get("parent_id"),
                child_ids=[],
                sequence=i.get("sequence"),
                note=i.get("note"),
                display_name=i.get("display_name"),
                is_active=True,
                is_manual=False,
                is_group=i.get("is_group"),
                is_template=False,
                is_postable=True,
            )
            input_data.append(new_account_account_data)
        if input_data:
            AccountAccount().insert_many(input_data)
