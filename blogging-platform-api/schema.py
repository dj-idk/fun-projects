from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import datetime
from typing import List, Optional


class PostBase(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    category: str = Field(...)
    tags: List[str]


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None

    @model_validator(mode="before")
    def check_at_least_one_field(cls, values):
        if not any(values.get(field) is not None for field in values):
            raise ValueError("At least one field must be provided.")
        return values


class PostInDB(BaseModel):
    id: int
    title: str = Field(...)
    content: str = Field(...)
    category: str = Field(...)
    tags: List[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
