from ninja import Schema
from pydantic import Field


class ChangePasswordSchema(Schema):
    current_password: str
    new_password: str = Field(min_length=10, max_length=128)


class TwoFactorSetupSchema(Schema):
    secret: str
    provisioning_uri: str


class TwoFactorVerifySchema(Schema):
    code: str = Field(min_length=6, max_length=6)


class TwoFactorStatusSchema(Schema):
    enabled: bool


class LoginTwoFactorSchema(Schema):
    email: str
    password: str
    code: str = Field(min_length=6, max_length=6)
