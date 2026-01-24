from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_URL = "postgresql://postgres:postgres974@localhost/MyDataBase"

engine = create_engine(SQLALCHEMY_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

# generator::w

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()