import aiohttp

from decimal import Decimal
from datetime import datetime, timezone

from fastapi import HTTPException, status

from .repository import BalanceRepository, TransactionRepository
from .schemas import TransactionHistoryRequestSchema
from .jwt import decode_token
from .config.log import logger


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
        
async def create_balance(params: dict) -> None:
    await BalanceRepository.add(params)
    return {"message": "gotovo"}

async def get_balance(user_id: int):
    balance = await BalanceRepository.filter({"user_id": user_id})
    return balance

def get_current_user_id(token: str):
    payload = decode_token(token)
    current_user_id = payload.get("id")
    return current_user_id

async def check_user_balance_exists(user_id: int) -> bool:
    try:
        user_balance = await get_balance(user_id)
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    if user_balance:
        return True
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User's balance doesn not exist")
    
async def check_balance_amount(user_id: int, amount: Decimal) -> bool:
    try:
        user_balance = await get_balance(user_id)
        if user_balance is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        if user_balance.amount >= amount:
            return True
        else:
            logger.error("Нужно больше золота")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нужно больше золота")
    except Exception as e:
        logger.error(f"{e}")
        raise e
    
async def make_transaction(producer_id: int, consumer_id: int, amount: Decimal):
    producer = await BalanceRepository.update({"user_id": producer_id, "amount": amount, "operation": False})
    consumer = await BalanceRepository.update({"user_id": consumer_id, "amount": amount, "operation": True})
    
    transaction = await TransactionRepository.add({
        "producer_id": producer.id,
        "consumer_id": consumer.id,
        "amount": amount,
        "status": True,
        "created_at": datetime.now(timezone.utc),
    })

    return transaction
    
async def filter_transactions(params: TransactionHistoryRequestSchema):
    transactions = await TransactionRepository.filter(params)
    return transactions