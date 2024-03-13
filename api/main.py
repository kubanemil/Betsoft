from db import session_dep
from fastapi import FastAPI, HTTPException
from models import Bet, BetCreate, BetRead
from sqlalchemy import select

app = FastAPI()


@app.post("/bet", response_model=BetRead)
async def create_bet(bet_create: BetCreate, session: session_dep):
    """
    Создает новую ставку.
    """
    bet = Bet(**bet_create.model_dump())
    session.add(bet)
    await session.commit()
    return bet


@app.get("/bets", response_model=list[BetRead])
async def get_bets(session: session_dep):
    """
    Получает список всех ставок.
    """
    return (await session.scalars(select(Bet))).all()


@app.put("/events/{event_id}", response_model=list[BetRead])
async def update_event(event_id: int, has_won: bool, session: session_dep):
    """
    Обновляет статус события и возвращает список ставок которые были свзязаны с ним.
    """
    bets = (await session.scalars(select(Bet).where(Bet.event_id == event_id))).all()

    if not bets:
        raise HTTPException(status_code=404, detail="Event not found")

    for bet in bets:
        bet.has_won = has_won
    await session.commit()
    return bets
