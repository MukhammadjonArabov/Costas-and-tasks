from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select, func

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)


async def show_main_menu(message: types.Message):
   keyboard = ReplyKeyboardMarkup(
       keyboard=[
            [KeyboardButton(text="💰 Harajatlar"), KeyboardButton(text="📝 Vazifalar")]
       ],
       resize_keyboard=True
   )
   await message.answer("🏠 Asosiy menyu:", reply_markup=keyboard)

async def phone_menu(message: types.Message):
   keyboard = ReplyKeyboardMarkup(
       keyboard=[
           [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)],
       ],
       resize_keyboard=True,
       one_time_keyboard=True
   )
   await message.answer(
       "👋 Salom! Iltimos, ro'yxatdan o'tish uchun telefon raqamingizni yuboring:",
       reply_markup=keyboard
   )

async def get_expanse_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Harajat qo'shish")],
            [KeyboardButton(text="📋 Harajatlar ro'yxati")],
            [KeyboardButton(text="📊 Harajatlar statistika")],
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

async def get_back_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("🔙 Menyuga qaytish")]
        ],
        resize_keyboard=True,
    )