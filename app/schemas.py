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