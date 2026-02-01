

from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    email: str =Field(min_length=8)
    password: str = Field(min_length=8)
