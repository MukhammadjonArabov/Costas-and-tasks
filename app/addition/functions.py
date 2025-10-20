from app.keyboards.expense_main import get_expanse_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import pytz
from aiogram import types
from app.database import User
from sqlalchemy import select



TZ = pytz.timezone('Asia/Tashkent')

class AddExpense(StatesGroup):
    amount = State()
    reason = State()
    date = State()

class DeleteExpense(StatesGroup):
    waiting_for_id = State()

class CustomState(StatesGroup):
    start_date = State()

async def back_to_manu(message: types.Message):
    await message.answer(
        "📋 Siz asosiy menyuga qaytdingiz.",
        reply_markup=get_expanse_keyboard(),
    )

async def cancel_adding_expense(message: types.Message, state: FSMContext):
    await state.clear()
    await back_to_manu(message)

async def get_user(session, telegram_id:int) -> User | None:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalars().first()
