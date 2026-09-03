from pydantic import BaseModel, Field, field_validator, field_serializer, computed_field, ConfigDict
from datetime import datetime
from typing import Optional


class ExpenseBaseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    amount: float = Field(
        ...,
        gt=0,
        validation_alias="expenseAmount",
        description="amount of the expense must be greater than 0"
    )
    currency: str = Field(
        default="USD",
        pattern=r"^[A-Z]{3}$",
        description="three letter currency code (USD, EUR, etc)"
    )
    description: str = Field(
        ...,
        min_length=3,
        max_length=150,
        description="description of the expense"
    )
    category_id: Optional[int] = Field(default=None, description="identifier of the category")

    @field_validator("description")
    def clean_ai_text(cls, value: str) -> str:
        cleaned = value.strip()
        if "here is" in cleaned.lower() or cleaned.lower() == "expense":
            raise ValueError("Expense description cannot contain 'here is' or 'expense'")
        return cleaned


class ExpenseInputSchema(ExpenseBaseSchema):
    pass


class ExpenseResponseSchema(ExpenseBaseSchema):
    id: str
    created_at: datetime

    @computed_field
    @property
    def ai_memory_summary(self) -> str:
        return f"[{self.id[:5]}] {self.description}: {self.amount} {self.currency}"

    @field_serializer("created_at")
    def format_date(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")