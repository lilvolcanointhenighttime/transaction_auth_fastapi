from dotenv import load_dotenv
from os import environ


load_dotenv()

DB_USER = environ["POSTGRES_USER_TRANSACTION"]
DB_PASSWORD = environ["POSTGRES_PASSWORD_TRANSACTION"]
DB_HOST = environ["POSTGRES_HOST_TRANSACTION"]
DB_PORT = environ["POSTGRES_PORT_TRANSACTION"]
DB_NAME = environ["POSTGRES_DB_TRANSACTION"]
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SECRET_KEY = environ["SECRET_KEY"]
ALGORITHM = environ["ALGORITHM"]