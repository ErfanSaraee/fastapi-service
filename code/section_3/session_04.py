from fastapi import FastAPI

app = FastAPI()

names_list = [
    {"id": 1, "name": "Amin"},
    {"id": 2, "name": "Maryam"},
    {"id": 3, "name": "Kiana"},
    {"id": 4, "name": "Soniya"},
    {"id": 5, "name": "Rasul"},
]


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/names")
def get_names():
    return names_list