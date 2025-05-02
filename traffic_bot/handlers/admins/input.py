import asyncio
import os
import re

from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import admin_data as db

from keyboards.reply import admin_menu

from data.config import LOG_CHANNEL_ID, ADM_TID, ADMIN_USER_ID

router = Router()


@router.message(F.text == "!", flags={"skip_logging": True})
async def admin_command(message: types.Message):
    if message.from_user.id in ADMIN_USER_ID:
        message_text = f"Успешная авторизация!"
        await message.reply(message_text, reply_markup=admin_menu())
