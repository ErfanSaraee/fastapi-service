from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from models.expense import Expense
from schemas.expense import ExpenseInputSchema, ExpenseResponseSchema

app = FastAPI(title="Expense Manager Project 03")


@app.post("/expenses", status_code=status.HTTP_201_CREATED, response_model=ExpenseResponseSchema)
def create_expense(expense_in: ExpenseInputSchema, db: Session = Depends(get_db)):
    db_expense = Expense(
        amount=expense_in.amount,
        currency=expense_in.currency,
        description=expense_in.description,
        category_id=expense_in.category_id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.get("/expenses", response_model=List[ExpenseResponseSchema], status_code=status.HTTP_200_OK)
def get_all_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()


@app.get("/expenses/{expense_id}", response_model=ExpenseResponseSchema, status_code=status.HTTP_200_OK)
def get_expense(expense_id: str, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter_by(id=expense_id).one_or_none()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense


@app.put("/expenses/{expense_id}", response_model=ExpenseResponseSchema, status_code=status.HTTP_200_OK)
def update_expense(expense_id: str, expense_in: ExpenseInputSchema, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter_by(id=expense_id).one_or_none()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    expense.amount = expense_in.amount
    expense.currency = expense_in.currency
    expense.description = expense_in.description
    expense.category_id = expense_in.category_id

    db.commit()
    db.refresh(expense)
    return expense


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: str, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter_by(id=expense_id).one_or_none()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    db.delete(expense)
    db.commit()