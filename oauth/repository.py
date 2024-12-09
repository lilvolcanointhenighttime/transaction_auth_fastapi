from .config.database import new_session
from fastapi import HTTPException, status
from .models import UserOrm
from sqlalchemy import select


class UserRepository():
    @classmethod
    async def add(cls, data: dict) -> dict:
        async with new_session() as session:
            user_orm = UserOrm(**data)
            session.add(user_orm)
            await session.flush()
            await session.commit()

            return {"id": user_orm.id, "email": user_orm.email}

    @classmethod
    async def return_all(cls):
        async with new_session() as session:
            query = select(UserOrm)
            result = await session.execute(query)

            users = result.scalars().all()
            return users
        
    @classmethod
    async def filter(cls, params: dict):
        async with new_session() as session:
            query = select(UserOrm)
            for key, value in params.items():
                if value:
                    query = query.filter(getattr(UserOrm, key) == value)
                    result = await session.execute(query)  
                else:
                    pass
            user = result.scalar_one_or_none()
            return user
    
    @classmethod
    async def update(cls, params: dict):
        email = params.get("email")
        new_password = params.get("new_password")
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.email == email)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
            if new_password:
                user.password_hash = new_password
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is empty")
            await session.commit()
            return user