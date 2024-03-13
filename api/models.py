from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from pydantic import BaseModel, validator
import datetime


class BaseTableModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Bet(BaseTableModel):
    event_id: Mapped[int]
    amount: Mapped[float]
    has_won: Mapped[bool | None]


class BetRead(BaseModel):
    id: int
    event_id: int
    amount: float
    has_won: bool | None


class BetCreate(BaseModel):
    event_id: int
    amount: float

    @validator("amount")
    def amount_is_positive(cls, v):
        if v <= 0:
            raise ValueError("amount must be positive")
        return v
    
    @validator("amount", pre=True)
    def round_amount(cls, v):
        if isinstance(v, float):
            return round(v, 2)
        return v