from pydantic import BaseModel, EmailStr, field_validator


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    def password_must_not_be_empty(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Password cannot be empty')
        return v


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
