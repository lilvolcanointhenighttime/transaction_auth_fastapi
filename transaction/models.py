from typing import Annotated
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from datetime import datetime
from decimal import Decimal


Base: DeclarativeMeta = declarative_base()

int_pk = Annotated[int, mapped_column(primary_key=True)]
int_uniq = Annotated[int, mapped_column(unique=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]

class UserBalanceOrm(Base):
    __tablename__ = "UserBalance"

    id: Mapped[int_pk]
    user_id: Mapped[int_uniq]
    amount: Mapped[Decimal]

class TransactionOrm(Base):
    __tablename__ = "Transactions"

    id: Mapped[int_pk]
    producer_id: Mapped[int]
    consumer_id: Mapped[int]
    amount: Mapped[Decimal]
    status: Mapped[bool]
    created_at: Mapped[created_at]