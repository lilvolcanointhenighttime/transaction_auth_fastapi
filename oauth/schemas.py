from pydantic import BaseModel, EmailStr


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr

class ChangePasswordSchema(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str