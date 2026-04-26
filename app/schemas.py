
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, model_validator

# CalculationUpdate schema (moved below imports)
class CalculationUpdate(BaseModel):
    a: float
    b: float
    type: Literal["Add", "Sub", "Multiply", "Divide"]

    @model_validator(mode="after")
    def check_division_by_zero(self):
        if self.type == "Divide" and self.b == 0:
            raise ValueError("Division by zero is not allowed.")
        return self

# User Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }

# Calculation Schemas
class CalculationCreate(BaseModel):
    a: float
    b: float
    type: Literal["Add", "Sub", "Multiply", "Divide"]

    @model_validator(mode="after")
    def check_division_by_zero(self):
        if self.type == "Divide" and self.b == 0:
            raise ValueError("Division by zero is not allowed.")
        return self

class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: str
    result: Optional[float] = None
    user_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }