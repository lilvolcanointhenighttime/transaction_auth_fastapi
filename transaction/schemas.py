from pydantic import BaseModel
from datetime import datetime


class CreateBalanceSchema(BaseModel):
    user_id: str

class TransactionSchema(BaseModel):
    id: int
    producer_id: int
    consumer_id: int
    amount: float
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class TransactionRequestSchema(BaseModel):
    consumer_id: int
    amount: float
    status: str
    created_at: datetime

class TransactionHistoryRequestSchema(BaseModel):
    page: int
    limit: int
    start_date: datetime
    end_date: datetime
    status: bool