import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app import crud, schemas

SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def setup_test_db():
    db = TestingSessionLocal()
    try:
        if not crud.get_api_collections(db):
            sample1 = schemas.APICollectionCreate(
                name_of_the_api="Sample API 1",
                postman_collection_json='{"info":{"name":"Sample API 1"},"item":[]}'
            )
            sample2 = schemas.APICollectionCreate(
                name_of_the_api="Sample API 2",
                postman_collection_json='{"info":{"name":"Sample API 2"},"item":[]}'
            )
            crud.create_api_collection(db, sample1)
            crud.create_api_collection(db, sample2)
    finally:
        db.close()


def test_health():
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_list_apis():
    setup_test_db()
    response = client.get("/v1/apis")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_api_by_id():
    setup_test_db()
    response = client.get("/v1/apis/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_get_api_by_name():
    setup_test_db()
    response = client.get("/v1/apis/name/Sample API 1")
    assert response.status_code == 200
    data = response.json()
    assert data["name_of_the_api"] == "Sample API 1"


def test_get_api_collection():
    setup_test_db()
    response = client.get("/v1/apis/1/collection")
    assert response.status_code == 200


def test_search_apis():
    setup_test_db()
    response = client.get("/v1/apis/search", params={"query": "Sample"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2