from pydantic import BaseModel, field_validator, Field, field_serializer


class BasePersonSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=50,
                      description="The name of the person")

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) < 3 or len(value) > 50:
            raise ValueError("Name must be between 3 and 50 characters")
        if not value.isalpha():
            raise ValueError("Name must contain only letters")
        return value

    @field_serializer("name")
    def serialize_name(self, value):
        return value.upper()


class PersonCreateSchema(BasePersonSchema):
    pass


class PersonResponseSchema(BasePersonSchema):
    id: int = Field(..., title="The ID of the person")


class PersonUpdateSchema(BasePersonSchema):
    pass
