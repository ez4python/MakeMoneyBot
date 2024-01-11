from sqlalchemy import select, update
from db import User, session
import asyncio


async def check_user_id(txt: str, user_id: int):
    txt = txt.split()
    user: User | None = session.execute(select(User).where(User.user_id == user_id)).fetchone()
    if len(txt) == 2 and not user:
        query = update(User).where(User.user_id == txt[1]).values(balance=User.balance + 200)
        session.execute(query)
        session.commit()


async def withdraw_money(user_id: int):
    pass


async def get_user_balance(user_id: int):
    balance = session.execute(select(User.balance).where(User.user_id == user_id)).one()[0]
    return balance
