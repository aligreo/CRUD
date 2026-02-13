from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

if not os.path.exists("./db"):
    os.makedirs("./db")
    
# Create the SQLite DB file
engine = create_engine("sqlite:///./db/tasks.db")
SessionLocal = sessionmaker(engine)
Base = declarative_base()

# Our Database Model
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    is_completed = Column(Boolean, default=False)

# Create the tables
Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()