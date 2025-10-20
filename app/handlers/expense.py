from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from datetime import datetime
from app.addition.functions import AddExpense, cancel_adding_expense, TZ, get_user
from app.keyboards.expense_main import get_back_keyboard, get_expanse_keyboard
from app.database import async_session, Expense


router = Router()

@router.message(F.text.contains("Harajatlar"))
async def expense_menu(message: types.Message):
   text = message.text

   if text == "➕ Harajat qo'shish":
       await add_expense_start(message)

   else:
       await message.answer(
           "💰 Harajatlar bo'limiga o'tdingiz. Quyidagilardan birini tanlang:",
           reply_markup=await get_expanse_keyboard()
       )



@router.message(F.text("➕ Harajat qo'shish"))
async def add_expense_start(message: types.Message, state: FSMContext):
   await message.answer(
       "💰 Harajat summasini kiriting (faqat musbat butun son):",
       reply_markup= await get_back_keyboard()
   )
   await state.set_state(AddExpense.amount)

@router.message(AddExpense.amount)
async def add_expense_amount(message: types.Message, state: FSMContext):
    if message.text == "🔙 Menyuga qaytish":
        await cancel_adding_expense(message, state)
        return
    try:
        amount = int(message.text.strip())
        if amount < 0:
            raise ValueError
        await state.update_data(amount=amount)
        await message.answer(
            """
            📝 Harajat sababini kiriting.\n
            Agar sabab bo‘lmasa, '-' belgini kiriting!
            """,
            reply_markup=await get_back_keyboard()
        )
        await state.set_state(AddExpense.amount)
    except ValueError:
        await message.answer("🚫 Iltimos, to‘g‘ri musbat butun son kiriting!")

@router.message(AddExpense.reason)
async def add_expense_reason(message: types.Message, state: FSMContext):
    if message.text == "🔙 Menyuga qaytish":
        await cancel_adding_expense(message, state)
        return

    reason = message.text.strip()
    reason = None if reason == "-" else reason

    await state.update_data(reason=reason)
    await message.answer(
        """
        📅 Sana va vaqtni kiriting (masalan: 2025-10-14 14:30)\n
        Hozirgi vaqtni kiritish uchun '-' belgini kiriting!
        """,
        reply_markup=await get_back_keyboard()
    )
    await state.set_state(AddExpense.reason)

@router.message(AddExpense.date)
async def add_expense_date(message: types.Message, state: FSMContext):
    if message.text == "🔙 Menyuga qaytish":
        await cancel_adding_expense(message, state)
        return

    date = await state.get_data()
    telegram_id = message.from_user.id

    if message.text.strip() == "-":
        created_at = datetime.now(TZ)
    else:
        try:
            created_at = TZ.localize(datetime.strptime(message.text.strip(), "%Y-%m-%d %H:%M"))
        except ValueError:
            await message.answer("🚫 Noto‘g‘ri format! Masalan: 2025-10-14 14:30 yoki '-' belgini kiriting.")

    if created_at > datetime.now(TZ):
        await message.answer("🚫 Kelajakdagi vaqtni kiritib bo‘lmaydi.")
        return

    async with async_session() as session:
        user = await get_user(session, telegram_id)
        if not user:
            await message.answer("❗ Avval ro‘yxatdan o‘ting! /start")
            await state.clear()
            return

        expense = Expense(
            user_id=user.id,
            amount=date["amount"],
            reason=date["reason"],
            created_at=created_at,
        )
        session.add(expense)
        await session.commit()
        await session.refresh(expense)

        await message.answer(
            f"✅ Harajat muvaffaqiyatli saqlandi!\n\n"
            f"🆔 ID: {expense.id}\n"
            f"💰 Miqdor: {expense.amount}\n"
            f"📝 Sabab: {expense.reason or 'Noma’lum'}\n"
            f"📅 Sana: {expense.created_at.strftime('%Y-%m-%d %H:%M')}",
            reply_markup=await get_expanse_keyboard()
        )
        await state.clear()


