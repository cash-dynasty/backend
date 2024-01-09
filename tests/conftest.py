import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


sys.path.append(".")
sys.path.append("./app")


from database import SQLALCHEMY_DATABASE_URL  # noqa: E402

from app.models.config import metadatas  # noqa: E402


@pytest.fixture(scope="session")
def engine():
    return create_engine(SQLALCHEMY_DATABASE_URL)


@pytest.fixture(scope="session")
def tables(engine):
    for metadata in metadatas:
        metadata.create_all(engine)
    yield
    # for metadata in metadatas:
    #     metadata.drop_all(engine)


@pytest.fixture
def dbsession(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()
