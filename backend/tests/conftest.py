import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DB_URL = "sqlite:///./test_recipes.db"   # file-based so connections share it

test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Patch BEFORE any other import touches models.database
import models.database as db_module
db_module.engine      = test_engine
db_module.SessionLocal = TestingSession

from models.database import Base
Base.metadata.create_all(bind=test_engine)
