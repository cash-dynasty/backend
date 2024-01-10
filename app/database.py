from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Musiałem dodać tutaj app. przed settingsami, bo inaczej nie działało przy "alembic check".
# Spróbuj jeszcze u siebie
#
# File "/Users/marcinwiatrak/Dev/cashdynasty/backend/app/database.py", line 1, in <module>
# from settings import settings
# ModuleNotFoundError: No module named 'settings'
from app.settings import settings


SQLALCHEMY_DATABASE_URL = settings.POSTGRESQL_CONNECTION_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
