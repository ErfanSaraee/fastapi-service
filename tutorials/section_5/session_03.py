from fastapi import FastAPI, Query, status, HTTPException, Path, Form, Body, File, UploadFile
from fastapi.responses import JSONResponse
from typing import Optional, Annotated, List
from contextlib import asynccontextmanager
from dataclasses import dataclass
from schemas_03 import *
from typing import List


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting...")
    yield
    print("Application is shutting down...")

app = FastAPI(lifespan=lifespan)

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


@app.get("/names", response_model=List[PersonResponseSchema])
def get_names(q: Annotated[str, Query(deprecated=True, alias="name", description="The name to search for", examples="Amin", max_length=50)] = None):
    if q:
        return [name for name in names_list if q.lower() in name["name"].lower()]
    return names_list


# @app.get("/names")
# def get_names(q: str | None = Query(default=None, min_length=50)):
#     if q:
#         return [name for name in names_list if q.lower() in name["name"].lower()]
#     return names_list



@app.post("/names", response_model=PersonResponseSchema, status_code=status.HTTP_201_CREATED)
def add_name(person: PersonCreateSchema):
    new_student = {"id": len(names_list) + 1,
                   "name": person.name}
    names_list.append(new_student)
    return new_student


@app.put("/names/{name_id}", response_model=PersonResponseSchema, status_code=status.HTTP_200_OK)
def update_name(person: PersonUpdateSchema, name_id: int = Path(..., title="The ID of the name to get", ge=1)):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = person.name
            return item

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Name not found")


@app.delete("/names/{name_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_name(name_id: int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return JSONResponse(content={"message": "Name deleted successfully"}, status_code=status.HTTP_200_OK)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Name not found")


@app.get("/names/{name_id}", response_model=PersonResponseSchema)
def get_name(name_id: int = Path(..., title="The ID of the name to get", ge=1)):
    for name in names_list:
        if name["id"] == name_id:
            return name

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Name not found")


@app.get("/")
def root():
    return JSONResponse(content={"message": "Hello World!"}, status_code=status.HTTP_200_OK)


# @app.post("/upload_files/")
# async def upload_file(file: bytes = File(...)):
#     return {"file_size": len(file)}


@app.post("/upload_files/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    print(file.__dict__)
    return {"file_name": file.filename, "content_type": file.content_type, "file_size": len(content)}
