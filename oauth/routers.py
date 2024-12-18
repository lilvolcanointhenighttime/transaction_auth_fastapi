import bcrypt
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status, Response

from .config.log import logger
from .schemas import ChangePasswordSchema, UserAuthSchema, UserResponseSchema
from .jwt import create_access_token, get_token, decode_token
from .utils import (user_registration, 
                    user_authentication, 
                    filter_user, hash_password, 
                    change_user, async_query_get)


router = APIRouter(tags=["auth"])

@router.post("/registration", response_model=UserResponseSchema)
async def registration(request: UserAuthSchema) -> UserResponseSchema:
    logger.info(f"Registering user: {request.email}")
    try:
        new_user = await user_registration(request)
        params = {"user_id": new_user.get("id")}
        print(params)
        await async_query_get("http://nginx/api/transaction/create-balance", params=params)
        return new_user
    except Exception as e:
        logger.error(f"Error while registering user: {e}")
        raise e

@router.post("/login")
async def login(response: Response, request: UserAuthSchema) -> Response:
    logger.info(f"Attempting to login to account: {request.email}")
    try:
        user = await user_authentication(request)
        access_token = create_access_token(payload={"id": user.id})
        logger.info(f"User {user.email} successfully logged in.")
        response.set_cookie(key="users_access_token", value=access_token, httponly=True)
        return {"message": "gotovo"}
    
    except Exception as e:
        logger.error(f"Error {request.email}: {e}")
        raise e

@router.post("/change-password")
async def change_password(request: ChangePasswordSchema, token: str = Depends(get_token)) -> Dict[str, str]:

    try:
        email: str = request.email
        logger.info(f"Changing password for: {email}")
    except Exception as e:
        logger.error(f"JWT error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    user = await filter_user({"email":email})
    if user is None:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    if not bcrypt.checkpw(request.old_password.encode(), user.password_hash.encode()):
        logger.error(f"Wrong password.")
        raise HTTPException(status_code=400, detail="Wrong password.")

    try:
        await change_user({"email": user.email, "new_password": hash_password(request.new_password)})
        logger.info(f"User: {email} successfully changed password.")
        return {"message": "Password changed successfully"}
    except Exception as e:
        logger.error(f"{e}")
        raise e

@router.get("/current-user")
async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = decode_token(token)
        user_id = payload.get("id")
        if user_id:
            logger.info(f"User: {user_id} hit /current-user endpoint")
            return {
                "id": user_id
            }
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e
