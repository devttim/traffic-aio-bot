import asyncio
import os
import re
from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from data import admin_data as db
from keyboards.reply import admin_menu
from data.config import LOG_CHANNEL_ID, ADM_TID, ADMIN_USER_ID

router = Router()


@router.message(F.text == "Блокировать пользователя", flags={"skip_logging": True})
async def show_admin_commands(message: types.Message):
    if message.from_user.id in ADMIN_USER_ID:
        message_func = "<b>Временно недоступно.</b>"
        await message.answer(message_func)
    else:
        await message.reply("У вас нет доступа к этой команде.")
