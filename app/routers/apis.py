from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "healthy"}


@router.get("/apis", response_model=list[schemas.APICollection])
def list_apis(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Listing APIs with skip={skip}, limit={limit}")
    apis = crud.get_api_collections(db, skip=skip, limit=limit)
    return apis


@router.get("/apis/{api_id}", response_model=schemas.APICollection)
def get_api_by_id(api_id: int, db: Session = Depends(get_db)):
    logger.info(f"Getting API by id={api_id}")
    db_api = crud.get_api_collection_by_id(db, api_id=api_id)
    if db_api is None:
        logger.warning(f"API with id={api_id} not found")
        raise HTTPException(status_code=404, detail="API not found")
    return db_api


@router.get("/apis/name/{name}", response_model=schemas.APICollection)
def get_api_by_name(name: str, db: Session = Depends(get_db)):
    logger.info(f"Getting API by name={name}")
    db_api = crud.get_api_collection_by_name(db, name=name)
    if db_api is None:
        logger.warning(f"API with name={name} not found")
        raise HTTPException(status_code=404, detail="API not found")
    return db_api


@router.get("/apis/{api_id}/collection")
def get_api_collection(api_id: int, db: Session = Depends(get_db)):
    logger.info(f"Getting collection for API id={api_id}")
    db_api = crud.get_api_collection_by_id(db, api_id=api_id)
    if db_api is None:
        logger.warning(f"API with id={api_id} not found")
        raise HTTPException(status_code=404, detail="API not found")
    return db_api.postman_collection_json


@router.get("/apis/search", response_model=list[schemas.APICollection])
def search_apis(query: str, db: Session = Depends(get_db)):
    logger.info(f"Searching APIs with query={query}")
    apis = crud.get_api_collections_by_search(db, query=query)
    return apis