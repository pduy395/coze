from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)  #, connect_args={"check_same_thread": False}

# with engine.connect() as connection:
#     connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


Base = declarative_base()

def get_postgresql():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

url: str = SUPABASE_URL
key: str = SUPABASE_SECRET_KEY

def get_supabase():
    supabase: Client = create_client(url, key)
    return supabase