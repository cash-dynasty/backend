import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

POSTGRESQL_CONNECTION_URL = os.environ.get("POSTGRESQL_CONNECTION_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))