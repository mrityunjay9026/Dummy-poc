from sqlalchemy.orm import Session
from . import models, schemas


def get_api_collections(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.APICollection).offset(skip).limit(limit).all()


def get_api_collection_by_id(db: Session, api_id: int):
    return db.query(models.APICollection).filter(models.APICollection.id == api_id).first()


def get_api_collection_by_name(db: Session, name: str):
    return db.query(models.APICollection).filter(models.APICollection.name_of_the_api == name).first()


def get_api_collections_by_search(db: Session, query: str):
    return db.query(models.APICollection).filter(models.APICollection.name_of_the_api.contains(query)).all()


def create_api_collection(db: Session, api_collection: schemas.APICollectionCreate):
    db_item = models.APICollection(**api_collection.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_personal_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PersonalData).offset(skip).limit(limit).all()


def get_personal_data_by_id(db: Session, person_id: int):
    return db.query(models.PersonalData).filter(models.PersonalData.id == person_id).first()


def get_personal_data_by_email(db: Session, email: str):
    return db.query(models.PersonalData).filter(models.PersonalData.email == email).first()


def create_personal_data(db: Session, personal_data: schemas.PersonalDataCreate):
    db_item = models.PersonalData(**personal_data.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item