from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select, func

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from sqlalchemy.orm import relationship


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
