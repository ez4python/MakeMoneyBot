import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy import select, insert

from reply import start_buttons
from db import User, session
from utils import check_user_id, withdraw_money, get_user_balance

BOT_TOKEN = "6408363442:AAFQdRmPBBJpTi1_S59VC6zppaFXDVTFGrA"
dp = Dispatcher(storage=MemoryStorage())


# https://t.me/illegal_testing_bot


class UserState(StatesGroup):
    advertising = State()


@dp.message(CommandStart())
async def start_handler(msg: types.Message):
    await check_user_id(msg.text, msg.from_user.id)
    user_data = {
        'user_id': msg.from_user.id,
        'first_name': msg.from_user.first_name,
        'last_name': msg.from_user.last_name,
        'username': msg.from_user.username
    }
    user: User | None = session.execute(select(User).where(User.user_id == msg.from_user.id)).fetchone()
    if not user:
        query = insert(User).values(**user_data)
        session.execute(query)
        session.commit()
        await msg.answer('You are welcome 🤗', reply_markup=start_buttons())
    else:
        user = user[0]
        if not user.last_name:
            if not user.first_name:
                await msg.answer('Welcome, user!', reply_markup=start_buttons())
            await msg.answer(f'Welcome, {user.first_name}!', reply_markup=start_buttons())
        else:
            await msg.answer(f'Welcome, {user.first_name} {user.last_name}', reply_markup=start_buttons())


@dp.message(lambda msg: msg.text == '🔗 Rental link')
async def create_link(msg: types.Message):
    await msg.answer("Here's your rental link 👇")
    await msg.answer(text=f"https://t.me/illegal_testing_bot?start={msg.from_user.id}", reply_markup=start_buttons())


@dp.message(lambda msg: msg.text == '💰 My balance')
async def user_balance_handler(msg: types.Message):
    balance = await get_user_balance(msg.from_user.id)
    await msg.answer(text=f'Your balance 💳:   {balance}$')


@dp.message(Command('advert'))
async def advert_cmd_handler(msg: types.Message, state: FSMContext):
    if msg.from_user.id == 1998050207:
        await state.set_state(UserState.advertising)
        await msg.answer('Send me ad-message 🚀')
    else:
        await msg.answer("Sorry, but you aren't admin)")


@dp.message(UserState.advertising)
async def advertising_handler(msg: types.Message):
    users = session.query(User).all()
    for user in users:
        await msg.copy_to(user.user_id)


async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
