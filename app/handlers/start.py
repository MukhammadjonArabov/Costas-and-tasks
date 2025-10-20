from aiogram import Router,types, F
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.exc import IntegrityError
from aiogram.filters import Command
from app.keyboards.expense_main import show_main_menu, phone_menu
from app.database import async_session, User
from sqlalchemy import select

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    tg_id = message.from_user.id
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == tg_id))
        user = result.scalars().first()

    if user:
        await show_main_menu(message)
    else:
        await phone_menu(message)

@router.message(F.contact)
async def contact_handler(message: types.Message):
    contact = message.contact
    tg_id = message.from_user.id
    username = message.from_user.username
    user_link = f"https://t.me/{username}" if username else None
    phone = contact.phone_number

    async with async_session() as session:
        user = User(
            telegram_id=tg_id,
            username=username,
            user_link=user_link,
            phone=phone,

        )
        session.add(user)

        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            await message.answer("❗ Siz allaqachon ro'yxatdan o'tgansiz")
            await show_main_menu(message)
            return

    await message.answer("✅ Ro'yxatdan o'tdingiz!", reply_markup=ReplyKeyboardRemove())
    await show_main_menu(message)

