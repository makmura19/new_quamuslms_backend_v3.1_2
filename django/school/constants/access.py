from enum import Enum
from typing import Set


class Role(str, Enum):

    SUPERADMIN = "superadmin"
    ALL = "*"
    PUBLIC = "__public__"

    ADMINISTRATOR = "admin"
    STUDENT = "student"
    TEACHER = "teacher"
    QURAN_COORDINATOR = "quran_coordinator"
    TAHFIDZ_TEACHER = "tahfidz_teacher"
    TAHFIDZ_COORDINATOR = "tahfidz_coordinator"
    TAHFIDZ_EXAMINER = "tahfidz_examiner"
    TAHFIDZ_JUZIYAH_EXAMINER = "tahfidz_juziyah_examiner"
    TAHSIN_TEACHER = "tahsin_teacher"
    TAHSIN_COORDINATOR = "tahsin_coordinator"
    TAHSIN_EXAMINER = "tahsin_examiner"
    PRA_TAHSIN_TEACHER = "pra_tahsin_teacher"
    PRA_TAHSIN_COORDINATOR = "pra_tahsin_coordinator"
    PRA_TAHSIN_EXAMINER = "pra_tahsin_examiner"
    ARABIC_TEACHER = "arabic_teacher"
    HOMEROOM = "homeroom"
    PRINCIPAL = "principal"
    FINANCE = "finance"
    MERCHANT = "merchant"
    STAFF_MANAGER = "staff_manager"
    STAFF_FINANCE = "staff_finance"
    STAFF_MARKETING = "staff_marketing"
    STAFF_ADMIN = "staff_admin"
    PPDB_ADM = "ppdb_adm"
    PPDB_VALIDATOR = "ppdb_validator"
    PPDB_CASHIER = "ppdb_cashier"
    PPDB_CHECKER = "ppdb_checker"
    PPDB_UNIT_COORDINATOR = "ppdb_unit_coordinator"
    PPDB_UNIT_STAFF = "ppdb_unit_staff"
    PPDB_FINANCE = "ppdb_finance"
    PPDB_DORMITORY_STAFF = "ppdb_dormitory_staff"
    PPDB_MEDIC = "ppdb_medic"
    HOLDING_LEADER = "holding_leader"
    HOLDING_ADMIN = "holding_admin"
    HOLDING_FINANCE = "holding_finance"
    HOLDING_STAFF = "holding_staff"
    HOLDING_CASHIER = "holding_cashier"


SCHOOL_ROLES: Set[str] = {
    Role.ADMINISTRATOR.value,
    Role.STUDENT.value,
    Role.TEACHER.value,
    Role.QURAN_COORDINATOR.value,
    Role.TAHFIDZ_TEACHER.value,
    Role.TAHFIDZ_COORDINATOR.value,
    Role.TAHFIDZ_EXAMINER.value,
    Role.TAHFIDZ_JUZIYAH_EXAMINER.value,
    Role.TAHSIN_TEACHER.value,
    Role.TAHSIN_COORDINATOR.value,
    Role.TAHSIN_EXAMINER.value,
    Role.PRA_TAHSIN_TEACHER.value,
    Role.PRA_TAHSIN_COORDINATOR.value,
    Role.PRA_TAHSIN_EXAMINER.value,
    Role.ARABIC_TEACHER.value,
    Role.HOMEROOM.value,
    Role.PRINCIPAL.value,
    Role.FINANCE.value,
}


HOLDING_ROLES: Set[str] = {
    Role.HOLDING_ADMIN.value,
    Role.HOLDING_CASHIER.value,
    Role.HOLDING_FINANCE.value,
}


class Action(str, Enum):
    LIST = "list"
    CREATE = "create"
    RETRIEVE = "retrieve"
    UPDATE = "update"
    DESTROY = "destroy"
