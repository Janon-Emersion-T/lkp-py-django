from datetime import datetime
from uuid import UUID

from ninja import Schema
from pydantic import EmailStr, Field


class RoleSummarySchema(Schema):
    id: UUID
    name: str
    slug: str


class UserListSchema(Schema):
    id: int
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    phone: str
    job_title: str
    department: str
    is_active: bool
    is_staff: bool
    last_login: datetime | None


class UserDetailSchema(UserListSchema):
    timezone: str
    preferred_language: str
    must_change_password: bool
    date_joined: datetime
    roles: list[RoleSummarySchema]


class UserCreateSchema(Schema):
    email: EmailStr
    username: str = Field(min_length=3, max_length=150)
    password: str = Field(min_length=10, max_length=128)
    first_name: str = Field(default="", max_length=150)
    last_name: str = Field(default="", max_length=150)
    phone: str = Field(default="", max_length=30)
    job_title: str = Field(default="", max_length=150)
    department: str = Field(default="", max_length=150)
    role_ids: list[UUID] = Field(default_factory=list)
    is_active: bool = True
    is_staff: bool = False


class UserUpdateSchema(Schema):
    first_name: str = Field(default="", max_length=150)
    last_name: str = Field(default="", max_length=150)
    phone: str = Field(default="", max_length=30)
    job_title: str = Field(default="", max_length=150)
    department: str = Field(default="", max_length=150)
    timezone: str = Field(default="Asia/Colombo", max_length=64)
    preferred_language: str = Field(default="en", max_length=10)
    is_active: bool = True
    is_staff: bool = False
