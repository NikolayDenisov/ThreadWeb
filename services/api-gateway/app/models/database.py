from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@db:5432/example"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
