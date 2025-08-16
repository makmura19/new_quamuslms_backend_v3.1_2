from dataclasses import dataclass, field
from typing import Optional
from marshmallow import Schema, fields as ma_fields
from utils.string_util import StringUtil


@dataclass(kw_only=True)
class AuthenticationUserData:
    school_id: Optional[str] = field(default="")
    holding_id: Optional[str] = field(default="")
    school_code: Optional[str] = field(default="")
    identity_number: Optional[str] = field(default="")
    username: str
    password: Optional[str] = field(
        default_factory=lambda: StringUtil.generate_code("nnnnn")
    )
    role: str
    is_staff: Optional[bool] = field(default=False)
    is_active: Optional[bool] = field(default=True)
    is_company_active: Optional[bool] = field(default=True)


class AuthenticationUserSchema(Schema):
    school_id = ma_fields.String(required=False, allow_none=True)
    holding_id = ma_fields.String(required=False, allow_none=True)
    school_code = ma_fields.String(required=False, allow_none=True)
    identity_number = ma_fields.String(required=False, allow_none=True)
    username = ma_fields.String(required=False, allow_none=True)
    password = ma_fields.String(required=False, allow_none=True)
    role = ma_fields.String(required=False, allow_none=True)
    is_staff = ma_fields.Boolean(required=False)
    is_active = ma_fields.Boolean(required=False)
    is_company_active = ma_fields.Boolean(required=False)
