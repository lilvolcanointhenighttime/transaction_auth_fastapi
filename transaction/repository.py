from fastapi import HTTPException, status
from sqlalchemy import select

from .config.database import new_session
from .schemas import TransactionHistoryRequestSchema
from .models import UserBalanceOrm, TransactionOrm


class BalanceRepository():
    @classmethod
    async def add(cls, data: dict) -> None:
        async with new_session() as session:
            data["amount"] = 0
            user_balance_orm = UserBalanceOrm(**data)
            session.add(user_balance_orm)
            await session.flush()
            await session.commit()
            return user_balance_orm
        
    @classmethod
    async def filter(cls, params: dict) -> UserBalanceOrm:
        async with new_session() as session:
            query = select(UserBalanceOrm)
            for key, value in params.items():
                if value:
                    query = query.filter(getattr(UserBalanceOrm, key) == value)
                    result = await session.execute(query)  
                else:
                    pass
            balance = result.scalar_one_or_none()
            return balance
    
    @classmethod
    async def update(cls, params: dict):
        async with new_session() as session:
            query = select(UserBalanceOrm).where(UserBalanceOrm.id == params.get("user_id"))
            result = await session.execute(query)
            balance = result.scalar_one_or_none()
            if not balance:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
            if params.get("operation") == True:
                balance.amount += params.get("amount")
            else:
                balance.amount -= params.get("amount")
            await session.commit()
            return balance

class TransactionRepository():
    @classmethod
    async def add(cls, data: dict) -> TransactionOrm:
        async with new_session() as session:
            transaction_orm = TransactionOrm(**data)
            session.add(transaction_orm)
            await session.flush()
            await session.commit()
            return transaction_orm
        

    @classmethod
    async def return_all(cls):
        async with new_session() as session:
            query = select(TransactionOrm)
            result = await session.execute(query)

            users = result.scalars().all()
            return users
    
    @classmethod
    async def filter(cls, params: TransactionHistoryRequestSchema) -> TransactionOrm:
        page = params.page
        limit = params.limit
        params = {"user_id": params.user_id,
        "start_date": params.start_date,
        "end_date": params.end_date,
        "status": params.status},

        async with new_session() as session:
            query = select(TransactionOrm)
            for key, value in params.items():
                if value:
                    if key == "start_date":
                        query = query.filter(TransactionOrm.created_at >= value)
                    if key == "end_date":
                        query = query.filter(TransactionOrm.created_at <= value)
                    query = query.filter(getattr(TransactionOrm, key) == value)
                    result = await session.execute(query)  
                else:
                    pass
        
            query = query.offset((page - 1) * limit).limit(limit)
            result = await session.execute(query)
            transactions = result.scalar_one_or_none()
            return transactions