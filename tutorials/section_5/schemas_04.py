from pydantic import BaseModel, field_validator


class BasePersonSchema(BaseModel):
    name: str

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) < 3 or len(value) > 50:
            raise ValueError("Name must be between 3 and 50 characters")
        if not value.isalpha():
            raise ValueError("Name must contain only letters")
        return value


class PersonCreateSchema(BasePersonSchema):
    pass


class PersonResponseSchema(BasePersonSchema):
    id: int


class PersonUpdateSchema(BasePersonSchema):
    pass


class Person(BaseModel):
    id: int
    name: str
    age: int


data1 = {
    "id": 1,
    "name": "Reza",
    "age": 30
}

data2 = '''
{
    "id": 1,
    "name": "Reza",
    "age": 30
}'''

p1 = Person.model_validate(data1)
p2 = Person.model_validate_json(data2)
