from pydantic import BaseModel
from datetime import datetime


class APICollectionBase(BaseModel):
    name_of_the_api: str
    postman_collection_json: str


class APICollectionCreate(APICollectionBase):
    pass


class APICollection(APICollectionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PersonalDataBase(BaseModel):
    name: str
    email: str
    bio: str
    age: int
    occupation: str


class PersonalDataCreate(PersonalDataBase):
    pass


class PersonalData(PersonalDataBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True