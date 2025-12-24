import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "test.db")
 
DATABASE_URL = f"sqlite:///{DB_PATH}"
 
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True
)
 
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()





# # from sqlalchemy import create_engine
# # from sqlalchemy.ext.declarative import declarative_base
# # from sqlalchemy.orm import sessionmaker

# # SQLALCHEMY_DATABASE_URL = "sqlite:///./data/app.db"


# # engine = create_engine(
# #     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# # )
# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base = declarative_base()


# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()


# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base  # SQLAlchemy 2.0 style

# SQLALCHEMY_DATABASE_URL = "sqlite:///./data/app.db"

# # For SQLite + threads (FastAPI/uvicorn), keep this arg
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

