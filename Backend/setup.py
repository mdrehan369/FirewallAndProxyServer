import os
from sqlalchemy import create_engine
from app.models import ModelBase
from dotenv import load_dotenv

load_dotenv()

databaseUrl = os.getenv("DATABASE_URL")

engine = create_engine(databaseUrl, echo=True)

ModelBase.metadata.create_all(engine)
print("Database created!")