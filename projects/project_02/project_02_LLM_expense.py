from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator, field_serializer, computed_field, ConfigDict
from datetime import datetime
from uuid import uuid4
from typing import List
import re


app = FastAPI()
expenses_db = {}


class ExpenseInputSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    amount: float = Field(..., gt=0,
                          validation_alias="expenseAmount",
                          description="amount of the expense must be greater than 0")
    currency: str = Field(
        default="USD", pattern=r"^[A-Z]{3}$", description="three letter currency code (USD, EUR, etc)")
    description: str = Field(..., min_length=3, max_length=150,
                             description="description of the expense")

    @field_validator("description")
    def clean_ai_text(cls, value: str) -> str:
        cleaned = value.strip()
        if "here is" in cleaned.lower() or "expense" == cleaned.lower():
            raise ValueError(
                "Expense description cannot contain 'here is' or 'expense'")
        return cleaned


class ExpenseResponseSchema(ExpenseInputSchema):
    id: str = Field(default_factory=lambda: uuid4().hex)
    created_at: datetime = Field(default_factory=datetime.now)

    @computed_field
    @property
    def ai_memory_summary(self) -> str:
        return f"[{self.id[:5]}] {self.description}: {self.amount} {self.currency}"

    @field_serializer("created_at")
    def format_date(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")


@app.post("/expenses", status_code=status.HTTP_201_CREATED, response_model=ExpenseResponseSchema)
def create_expense(expense: ExpenseInputSchema):
    new_expense = ExpenseResponseSchema(**expense.model_dump())
    expenses_db[new_expense.id] = new_expense
    return new_expense


@app.get("/expenses", response_model=list[ExpenseResponseSchema], status_code=status.HTTP_200_OK)
def get_all_expenses():
    return list(expenses_db.values())


@app.get("/expenses/{expense_id}", response_model=ExpenseResponseSchema, status_code=status.HTTP_200_OK)
def get_expense(expense_id: str):
    if expense_id not in expenses_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Expense not found")

    return expenses_db[expense_id]


'''
expenses_db = {
    "f81d4fae7dec4bc6ab92fb8d022b7a2a": ExpenseResponseSchema(
        id="f81d4fae7dec4bc6ab92fb8d022b7a2a",
        amount=15.5,
        currency="USD",
        description="خرید قهوه",
        created_at=datetime.datetime(2026, 9, 1, 18, 30, 0)
    ),
    "b29c8e103f5a431aa78d65198e3df911": ExpenseResponseSchema(
        id="b29c8e103f5a431aa78d65198e3df911",
        amount=120.0,
        currency="EUR",
        description="خرید کتاب هوش مصنوعی",
        created_at=datetime.datetime(2026, 9, 1, 19, 10, 0)
    )
}
'''


@app.put("/expenses/{expense_id}", response_model=ExpenseResponseSchema, status_code=status.HTTP_200_OK)
def update_expense(expense_id: str, expense: ExpenseInputSchema):
    if expense_id not in expenses_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Expense not found")

    expenses_db[expense_id].amount = expense.amount
    expenses_db[expense_id].currency = expense.currency
    expenses_db[expense_id].description = expense.description
    return expenses_db[expense_id]


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: str):
    if expense_id not in expenses_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Expense not found")

    del expenses_db[expense_id]
