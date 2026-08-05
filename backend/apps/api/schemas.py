from ninja import Schema


class LoginSchema(Schema):
    email: str
    password: str


class RefreshSchema(Schema):
    refresh: str


class TokenSchema(Schema):
    access: str
    refresh: str


class UserSchema(Schema):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    is_staff: bool


class LogoutSchema(Schema):
    refresh: str
