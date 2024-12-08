from dotenv import load_dotenv
from os import environ

load_dotenv()

DB_USER = environ["POSTGRES_USER_OAUTH"]
DB_PASSWORD = environ["POSTGRES_PASSWORD_OAUTH"]
DB_HOST = environ["POSTGRES_HOST_OAUTH_FASTAPI"]
DB_PORT = environ["POSTGRES_PORT_OAUTH"]
DB_NAME = environ["POSTGRES_DB_OAUTH"]
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SECRET_KEY = environ["SECRET_KEY"]
ALGORITHM = environ["ALGORITHM"]