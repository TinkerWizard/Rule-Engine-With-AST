from sqlmodel import SQLModel, Field, create_engine, Session, select
import os
from dotenv import load_dotenv
load_dotenv()
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
DATABASE_URL = f"postgresql://{username}:{password}@localhost:5432/rule_engine"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create the database and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
def get_session():
    with Session(engine) as session:
        yield session