from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


expenses_db = {}
current_id = 1


class ExpenseCreate(BaseModel):
    amount: float
    description: str


class ExpenseResponse(ExpenseCreate):
    id: int
    description: str
    amount: float


@app.post("/expenses", status_code=status.HTTP_201_CREATED, response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate):
    global current_id

    new_expense = {"id": current_id, "amount": expense.amount,
                   "description": expense.description}
    expenses_db[current_id] = new_expense
    current_id += 1
    return new_expense


@app.get("/expenses", response_model=list[ExpenseResponse], status_code=status.HTTP_200_OK)
def get_all_expenses():
    return list(expenses_db.values())


@app.get("/expenses/{expense_id}", response_model=ExpenseResponse, status_code=status.HTTP_200_OK)
def get_expense(expense_id: int):
    if expense_id not in expenses_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Expense not found")

    return expenses_db[expense_id]


@app.put("/expenses/{expense_id}", response_model=ExpenseResponse, status_code=status.HTTP_200_OK)
def update_expense(expense_id: int, expense: ExpenseCreate):
    if expense_id not in expenses_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Expense not found")

    expenses_db[expense_id]["amount"] = expense.amount
    expenses_db[expense_id]["description"] = expense.description

    return expenses_db[expense_id]


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int):
    if expense_id not in expenses_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Expense not found")

    del expenses_db[expense_id]
