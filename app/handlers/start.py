from aiogram import Router,types, F
from sqlalchemy.exc import IntegrityError
from aiogram.filters import Command
from app.keyboards.expense_main import show_main_menu
from app.database import async_session, User
from sqlalchemy import select

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    tg_id = message.from_user.id
    username = message.from_user.username

    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == tg_id))
        user = result.scalor().first()

    if user:
        await show_main_menu(message)
    else:

