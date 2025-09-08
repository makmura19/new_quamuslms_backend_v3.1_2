
from rest_framework.exceptions import ValidationError
from datetime import datetime, timezone
from models.edu_academic_year import EduAcademicYear
from models.edu_semester import EduSemester

class Utils:
    def __init__(self):
        self.now = datetime.now()
        self.academic_data = EduAcademicYear().find({})
        self.semester_data = EduSemester().find({})
        
    def active_academic_year(self):
        active_academic_year = [
            i for i in self.academic_data
            if datetime.strptime(i.get("start_date").split("T")[0], "%Y-%m-%d") <= self.now and
            datetime.strptime(i.get("end_date").split("T")[0], "%Y-%m-%d") > self.now
        ]
        if not active_academic_year:
            raise ValidationError("Tidak ada tahun akademik yang aktif untuk saat ini.")
        
        return {
            "_id": active_academic_year[0].get("_id"),
            "name": active_academic_year[0].get("name"),
            "short_name": active_academic_year[0].get("short_name"),
            "year": active_academic_year[0].get("year")
        }
        
    def active_semester(self):
        active_semester = [
            i for i in self.semester_data
            if datetime.strptime(i.get("start_date").split("T")[0], "%Y-%m-%d") <= self.now and
            datetime.strptime(i.get("end_date").split("T")[0], "%Y-%m-%d") > self.now
        ]
        if not active_semester:
            raise ValidationError("Tidak ada tahun akademik yang aktif untuk saat ini.")
        
        return {
            "_id": active_semester[0].get("_id"),
            "semester_no": active_semester[0].get("semester_no"),
            "name": active_semester[0].get("name")
        }