from typing import Annotated
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from datetime import datetime


Base: DeclarativeMeta = declarative_base()

int_pk = Annotated[int, mapped_column(primary_key=True)]
int_uniq = Annotated[int, mapped_column(unique=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]

class UserOrm(Base):
    __tablename__ = "User"

    id: Mapped[int_pk]
    email: Mapped[str_uniq]
    password_hash: Mapped[str]

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"