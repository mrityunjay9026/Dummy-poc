from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base


class APICollection(Base):
    __tablename__ = "api_collections"

    id = Column(Integer, primary_key=True, index=True)
    name_of_the_api = Column(String, index=True)
    postman_collection_json = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())