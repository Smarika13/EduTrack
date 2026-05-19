from pydantic import BaseModel, EmailStr, field_validator


class BaseUserSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str
    faculty: str
    password: str

    @field_validator('name')
    def name_must_be_valid(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters')
        return v.strip()

    @field_validator('phone')
    def phone_must_be_valid(cls, v):
        if not v.isdigit():
            raise ValueError('Phone must contain only digits')
        if len(v) != 10:
            raise ValueError('Phone must be exactly 10 digits')
        return v

    @field_validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

    @field_validator('faculty')
    def faculty_must_be_valid(cls, v):
        allowed = ['BCT', 'BEL', 'BCE', 'BME', 'BAG']
        if v.upper() not in allowed:
            raise ValueError(f'Faculty must be one of {allowed}')
        return v.upper()
