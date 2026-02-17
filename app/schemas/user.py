from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    is_active: bool
    is_stuff: bool


class UserRead(UserUpdate):
    id: int
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )
