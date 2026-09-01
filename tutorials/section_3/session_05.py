from fastapi import FastAPI

app = FastAPI()

names_list = [
    {"id": 1, "name": "Amin"},
    {"id": 2, "name": "Maryam"},
    {"id": 3, "name": "Kiana"},
    {"id": 4, "name": "Soniya"},
    {"id": 5, "name": "Rasul"},
]

@app.get("/names")
def get_names():
    return names_list


@app.get("/names/{name_id}")
def get_name(name_id: int):
    for name in names_list:
        if name["id"] == name_id:
            return name

    return {"error": "Name not found"}