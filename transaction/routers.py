from fastapi import APIRouter, Depends, HTTPException, status

from .config.log import logger
from .schemas import TransactionRequestSchema, TransactionHistoryRequestSchema
from .jwt import get_token
from .utils import (check_balance_amount, 
                    get_balance, 
                    create_balance, 
                    get_current_user_id, 
                    check_user_balance_exists, 
                    make_transaction, 
                    filter_transactions)


router = APIRouter(tags=["transaction"])

@router.get("/create-balance")
async def create_balance_endpoint(user_id: int):
    params = {
        "user_id": user_id
    }
    await create_balance(params)
    logger.info(f"Created balance for user: {user_id}")
    return {"message": "gotovo"}

@router.get("/balance")
async def get_balance_endpoint(token: str = Depends(get_token)):
    current_user_id = get_current_user_id(token)
    balance = await get_balance(current_user_id)
    return balance

@router.post("/transactions")
async def transfer(request: TransactionRequestSchema, token: str = Depends(get_token)) -> dict:
    if request.amount <= 0:
        logger.error("Amount should be positive")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount should be positive")
    logger.info("Beggining transactions")
    current_user_id = get_current_user_id(token)
    logger.info(f"User: {current_user_id} started transaction with {request.consumer_id}")
    try:
        _ = await check_user_balance_exists(request.consumer_id)
    except Exception as e:
        logger.error(f"{e}")
        raise e
    
    try:
        _ = await check_balance_amount(current_user_id, request.amount)
    except Exception as e:
        logger.error(f"{e}")
        raise e

    try:
        await make_transaction(producer_id=current_user_id, 
                         consumer_id=request.consumer_id,
                         amount=request.amount)
        logger.info(
            f"Перевод завершен: ID:{current_user_id} отправил сумму {request.amount} "
            f"ID:{request.consumer_id}"
        )
        balance = await get_balance(current_user_id)
        return {"message": "Transfer successful",
                "balance": balance.amount}
    except Exception as e:
        logger.error(f"Transaction failed: {e}")
        raise e

@router.get("/transaction-history")
async def get_transaction_history(requset: TransactionHistoryRequestSchema, token: str = Depends(get_token)) -> dict:
    current_user_id = get_current_user_id(token)
    try:
        balance_exists = await check_user_balance_exists(current_user_id)
        if not balance_exists:
            logger.error(f"Balance with ID {current_user_id} does not exist.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Balance does not exist")
        transactions = await filter_transactions(requset)
        if not transactions:
            logger.info(f"No transactions found for {current_user_id}.")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No transactions found for {current_user_id}.")
        return {
            "page": requset.page,
            "limit": requset.limit,
            "transactions": [transaction for transaction in transactions]
        }
    except HTTPException as e:
        logger.error(f"Error: {e.detail}")
        raise e