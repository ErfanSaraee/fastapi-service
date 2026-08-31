from fastapi import FastAPI, Query
from typing import Optional, Annotated

app = FastAPI()

names_list = [
    {"id": 1, "name": "Amin"},
    {"id": 2, "name": "Maryam"},
    {"id": 3, "name": "Kiana"},
    {"id": 4, "name": "Soniya"},
    {"id": 5, "name": "Rasul"},
    {"id": 6, "name": "Amin"},
    {"id": 7, "name": "Amin"},
]


# @app.get("/names")
# def get_names(q: str | None = None):
#     if q:
#         return [name for name in names_list if q.lower() in name["name"].lower()]
#     return names_list


# @app.get("/names")
# def get_names(q: Optional[str] = None):
#     if q:
#         return [name for name in names_list if q.lower() in name["name"].lower()]
#     return names_list


@app.get("/names")
def get_names(q: Annotated[str, Query(min_length=50)] = None):
    if q:
        return [name for name in names_list if q.lower() in name["name"].lower()]
    return names_list


# @app.get("/names")
# def get_names(q: str | None = Query(default=None, min_length=50)):
#     if q:
#         return [name for name in names_list if q.lower() in name["name"].lower()]
#     return names_list



@app.post("/names")
def add_name(name: str):
    names_list.append({"id": len(names_list) + 1, "name": name})
    return {"message": "Name added successfully"}


@app.put("/names/{name_id}")
def update_name(name_id: int, name: str):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = name
            return {"message": "Name updated successfully"}

    return {"error": "Name not found"}


@app.delete("/names/{name_id}")
def delete_name(name_id: int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return {"message": "Name deleted successfully"}

    return {"error": "Name not found"}


@app.get("/names/{name_id}")
def get_name(name_id: int):
    for name in names_list:
        if name["id"] == name_id:
            return name

    return {"error": "Name not found"}
