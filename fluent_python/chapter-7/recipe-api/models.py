from pydantic import BaseModel, Field


class Ingredient(BaseModel):

    name: str
    amount: float
    unit: str


class Recipe(BaseModel):

    id: int
    name: str
    cuisine: str
    difficulty: int = Field(..., gt=0, lt=6)
    prep_time: int = Field(..., gt=0)
    ingredients: list[Ingredient] = Field(...)
    instructions: str
