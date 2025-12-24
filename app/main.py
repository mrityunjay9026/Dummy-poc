from fastapi import FastAPI
from .database import engine
from . import models
from .routers import apis
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Collections Manager", version="1.0.0")

app.include_router(apis.router, prefix="/v1", tags=["apis"])

@app.on_event("startup")
def startup_event():
    logger.info("Application startup")
    # Seeding data
    from sqlalchemy.orm import sessionmaker
    from .crud import create_api_collection
    from .schemas import APICollectionCreate
    import json
    import os

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        # Check if already seeded
        from .crud import get_api_collections
        if not get_api_collections(db):
            # Load sample collections
            with open(os.path.join(os.path.dirname(__file__), "..", "postman", "sample1.postman_collection.json"), "r") as f:
                sample1_json = json.dumps(json.load(f))
            with open(os.path.join(os.path.dirname(__file__), "..", "postman", "sample2.postman_collection.json"), "r") as f:
                sample2_json = json.dumps(json.load(f))
            
            sample1 = APICollectionCreate(
                name_of_the_api="Sample API 1",
                postman_collection_json=sample1_json
            )
            sample2 = APICollectionCreate(
                name_of_the_api="Sample API 2",
                postman_collection_json=sample2_json
            )
            sample3 = APICollectionCreate(
                name_of_the_api="User Management API",
                postman_collection_json=json.dumps({
                    "info": {"name": "User Management API", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
                    "item": [
                        {"name": "Get Users", "request": {"method": "GET", "header": [], "url": {"raw": "{{base_url}}/users", "host": ["{{base_url}}"], "path": ["users"]}}},
                        {"name": "Create User", "request": {"method": "POST", "header": [], "url": {"raw": "{{base_url}}/users", "host": ["{{base_url}}"], "path": ["users"]}}}
                    ],
                    "variable": [{"key": "base_url", "value": "https://api.example.com"}]
                })
            )
            sample4 = APICollectionCreate(
                name_of_the_api="Product Catalog API",
                postman_collection_json=json.dumps({
                    "info": {"name": "Product Catalog API", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
                    "item": [
                        {"name": "List Products", "request": {"method": "GET", "header": [], "url": {"raw": "{{base_url}}/products", "host": ["{{base_url}}"], "path": ["products"]}}},
                        {"name": "Get Product", "request": {"method": "GET", "header": [], "url": {"raw": "{{base_url}}/products/{{product_id}}", "host": ["{{base_url}}"], "path": ["products", "{{product_id}}"]}}}
                    ],
                    "variable": [
                        {"key": "base_url", "value": "https://api.example.com"},
                        {"key": "product_id", "value": "123"}
                    ]
                })
            )
            sample5 = APICollectionCreate(
                name_of_the_api="Weather API",
                postman_collection_json=json.dumps({
                    "info": {"name": "Weather API", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
                    "item": [
                        {"name": "Current Weather", "request": {"method": "GET", "header": [], "url": {"raw": "{{base_url}}/weather?city={{city}}", "host": ["{{base_url}}"], "path": ["weather"], "query": [{"key": "city", "value": "{{city}}"}]}}}
                    ],
                    "variable": [
                        {"key": "base_url", "value": "https://api.weather.com"},
                        {"key": "city", "value": "New York"}
                    ]
                })
            )
            sample6 = APICollectionCreate(
                name_of_the_api="E-commerce API",
                postman_collection_json=json.dumps({
                    "info": {"name": "E-commerce API", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
                    "item": [
                        {"name": "Get All Products", "request": {"method": "GET", "header": [], "url": {"raw": "{{base_url}}/products", "host": ["{{base_url}}"], "path": ["products"]}}},
                        {"name": "Get Product by ID", "request": {"method": "GET", "header": [], "url": {"raw": "{{base_url}}/products/{{product_id}}", "host": ["{{base_url}}"], "path": ["products", "{{product_id}}"]}}},
                        {"name": "Create Product", "request": {"method": "POST", "header": [{"key": "Content-Type", "value": "application/json"}], "body": {"mode": "raw", "raw": "{\"name\": \"New Product\", \"price\": 99.99}"}, "url": {"raw": "{{base_url}}/products", "host": ["{{base_url}}"], "path": ["products"]}}},
                        {"name": "Update Product", "request": {"method": "PUT", "header": [{"key": "Content-Type", "value": "application/json"}], "body": {"mode": "raw", "raw": "{\"name\": \"Updated Product\", \"price\": 149.99}"}, "url": {"raw": "{{base_url}}/products/{{product_id}}", "host": ["{{base_url}}"], "path": ["products", "{{product_id}}"]}}},
                        {"name": "Delete Product", "request": {"method": "DELETE", "header": [], "url": {"raw": "{{base_url}}/products/{{product_id}}", "host": ["{{base_url}}"], "path": ["products", "{{product_id}}"]}}},
                        {"name": "Get User Cart", "request": {"method": "GET", "header": [], "url": {"raw": "{{base_url}}/users/{{user_id}}/cart", "host": ["{{base_url}}"], "path": ["users", "{{user_id}}", "cart"]}}},
                        {"name": "Add to Cart", "request": {"method": "POST", "header": [{"key": "Content-Type", "value": "application/json"}], "body": {"mode": "raw", "raw": "{\"product_id\": \"{{product_id}}\", \"quantity\": 1}"}, "url": {"raw": "{{base_url}}/users/{{user_id}}/cart", "host": ["{{base_url}}"], "path": ["users", "{{user_id}}", "cart"]}}}
                    ],
                    "variable": [
                        {"key": "base_url", "value": "https://api.ecommerce.com"},
                        {"key": "product_id", "value": "123"},
                        {"key": "user_id", "value": "456"}
                    ]
                })
            )
            create_api_collection(db, sample1)
            create_api_collection(db, sample2)
            create_api_collection(db, sample3)
            create_api_collection(db, sample4)
            create_api_collection(db, sample5)
            create_api_collection(db, sample6)
            
            # Seed personal data
            from .crud import create_personal_data, get_personal_data
            from .schemas import PersonalDataCreate
            if not get_personal_data(db):
                person1 = PersonalDataCreate(
                    name="John Doe",
                    email="john.doe@example.com",
                    bio="A software engineer passionate about AI and machine learning. Loves hiking and reading sci-fi novels.",
                    age=30,
                    occupation="Software Engineer"
                )
                person2 = PersonalDataCreate(
                    name="Jane Smith",
                    email="jane.smith@example.com",
                    bio="Marketing specialist with 5 years of experience in digital campaigns. Enjoys photography and traveling.",
                    age=28,
                    occupation="Marketing Specialist"
                )
                person3 = PersonalDataCreate(
                    name="Alice Johnson",
                    email="alice.johnson@example.com",
                    bio="Data scientist specializing in predictive analytics. Avid gamer and coffee enthusiast.",
                    age=32,
                    occupation="Data Scientist"
                )
                create_personal_data(db, person1)
                create_personal_data(db, person2)
                create_personal_data(db, person3)
                logger.info("Seeded personal data")
            
            logger.info("Seeded sample data")
    finally:
        db.close()
@app.on_event("shutdown")
def shutdown_event():  
    logger.info("Application shutdown")
    # Perform any necessary cleanup here
    pass
    logger.info("Application shutdown")

    
    