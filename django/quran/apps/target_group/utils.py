
from rest_framework.exceptions import ValidationError
from datetime import datetime, timezone
from models.edu_academic_year import EduAcademicYear

def active_academic_year():
    now = datetime.now()
    data = EduAcademicYear().find({})
    active_academic_year = [
        i for i in data
        if datetime.strptime(i.get("start_date").split("T")[0], "%Y-%m-%d") <= now and
        datetime.strptime(i.get("end_date").split("T")[0], "%Y-%m-%d") > now
    ]
    if not active_academic_year:
        raise ValidationError("Tidak ada tahun akademik yang aktif untuk saat ini.")
    
    return {
        "_id": active_academic_year[0].get("_id"),
        "name": active_academic_year[0].get("name"),
        "short_name": active_academic_year[0].get("short_name"),
        "year": active_academic_year[0].get("year")
    }