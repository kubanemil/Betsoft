from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select
import typing
from models import BetRead, BetCreate, Bet
import os


DATABASE_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
    os.environ["DB_USER"],
    os.environ["DB_PASSWORD"],
    os.environ["DB_HOST"],
    os.environ["DB_PORT"],
    os.environ["DB_NAME"],
)

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


app = FastAPI()


async def get_session():
    async with async_session() as session:
        yield session

session_dep = typing.Annotated[AsyncSession, Depends(get_session)]


@app.post("/bet", response_model=BetRead)
async def place_bet(bet_create: BetCreate, session: session_dep):
    bet = Bet(**bet_create.model_dump())
    session.add(bet)
    await session.commit()
    return bet


@app.get("/bets", response_model=list[BetRead])
async def get_bets(session: session_dep):
    return (await session.scalars(select(Bet))).all()


@app.put("/events/{event_id}", response_model=list[BetRead])
async def update_event(event_id: int, has_won: bool, session: session_dep):
    bets = (await session.scalars(select(Bet).where(Bet.event_id==event_id))).all()

    if not bets:
        raise HTTPException(status_code=404, detail="Event not found")

    for bet in bets:
        bet.has_won = has_won
    await session.commit()
    return bets

