import bcrypt
import aiohttp

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError    

from .config.log import logger
from .config.hash import SALT
from .models import UserOrm
from .schemas import UserAuthSchema
from .repository import UserRepository


async def async_query_post(url: str, headers: dict = {}, params: dict = {}) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(headers=headers, url=url, params=params) as response:
            data = await response.json()
            return data
    
async def async_query_get(url: str, headers: dict = {}, params: dict = {}) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(headers=headers, url=url, params=params) as response:
            data = await response.json()
            return data

def hash_password(password: str) -> str:
    if not password:
        raise ValueError("Password is empty.")

    try:
        password_hash = bcrypt.hashpw(password.encode(), salt=SALT)
        return password_hash.decode()
    except Exception as e:
        raise e

async def user_registration(requset: UserAuthSchema) -> dict:
    if not requset.email or not requset.password:
        logger.error("Email or password is empty.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or password is empty.")

    try:
        db_user = await filter_user({"email": requset.email})
        if db_user:
            logger.warning(f"Account with Email: {requset.email} already exists.")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Account with Email: {requset.email} already exists.")

        password_hash = hash_password(requset.password)
        new_user = await add_user({"email": requset.email, "password_hash": password_hash})

        logger.info(f"User {requset.email} successfully registered.")
        return new_user

    except Exception as e:
        logger.error(f"Error: {e}")
        raise e
    
async def user_authentication(requset: UserAuthSchema) -> UserOrm:
    email = requset.email
    password = hash_password(requset.password) 
    if not email or not password:
        logger.error("Email or password is empty.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or password is empty.")

    try:
        user = await filter_user({"email": email})

        if not user:
            logger.warning(f"User with email: {email} not found.")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email: {email} not found.")

        if not password.encode() == user.password_hash.encode():
            logger.warning("Wrong password.")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password.")

        logger.info(f"User with email: {email} successfully authenticated.")
        return user

    except Exception as e:
        logger.error(f"Error: {e}")
        raise e
    
async def add_user(params: dict) -> UserOrm:
    try:
        user = await UserRepository.add(params)
        if user:
            logger.info(f"User added.")
        else:
            logger.info(f"Error while adding user")
        return user

    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

async def filter_user(params: dict) -> UserOrm:
    try:
        user = await UserRepository.filter(params)
        if user:
            logger.info(f"User found.")
        else:
            logger.info(f"User not found")
        return user

    except SQLAlchemyError as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except ValueError as e:
        logger.warning(f"Invalid email address: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid email address: {e}")

async def change_user(params: dict) -> None: 
    try:
        await UserRepository.update(params)
        logger.info("User updated.")
    except SQLAlchemyError as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except ValueError as e:
        logger.warning(f"Invalid email address: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid email address: {e}")
