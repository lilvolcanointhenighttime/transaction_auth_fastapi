from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Request, HTTPException, status

from .config.env import SECRET_KEY, ALGORITHM
    

def get_auth_data():
    return {"secret_key": SECRET_KEY, "algorithm": ALGORITHM}

def create_access_token(payload: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    auth_data = get_auth_data()
    encode_jwt = jwt.encode({"exp": expire, **payload}, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt

def decode_token(token: str) -> dict:
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
        expire = payload.get('exp')
        expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
        if (not expire) or (expire_time < datetime.now(timezone.utc)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token
