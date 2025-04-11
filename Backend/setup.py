import os
from sqlalchemy import create_engine
from app.models import Base

databaseUrl = os.getenv("DATABASE_URL")

engine = create_engine(databaseUrl, echo=True)

Base.metadata.create_all(engine)
print("Database created!")