from datetime import timedelta, datetime

import aiohttp
from aiogram import Router, types, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import data.user_data as db
import keyboards.inline as inl_kb

router = Router()


@router.callback_query(F.data == "resources")
async def handler_offers(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    language = db.get_user_language(callback.from_user.id)
    balance = await db.get_user_balance(user_id)
    if language == "ua":
        message_text = (
            f"Лінкач має крутий функціонал, який вразить тебе своєю простотою та ефективністю. 😉  Хочеш дізнатися більше? Підписуйся на наші ресурси і  першим отримуй всю info про Лінкач та його можливості! 🤫"
            f"\n\n"
            f"Не гаєш часу - підписуйся зараз! 👇"
        )

        photo_path = FSInputFile("./data/images/res_ua.JPG")
        await bot.send_photo(
            callback.from_user.id,
            photo=photo_path,
            caption=message_text,
            parse_mode="HTML",
            reply_markup=inl_kb.keyboard_resources(user_id),
        )
    else:
        message_text = (
            f"Линкач имеет крутой функционал, который поразит тебя своей простотой и эффективностью. 😉 Хочешь узнать больше? Подписывайся на наши ресурсы и первым получай всю информацию о Линкач и его возможностях! 🤫"
            f"\n\n"
            f"Не теряй время — подписывайся сейчас! 👇"
        )

        photo_path = FSInputFile("./data/images/res_ru.JPG")
        await bot.send_photo(
            callback.from_user.id,
            photo=photo_path,
            caption=message_text,
            parse_mode="HTML",
            reply_markup=inl_kb.keyboard_resources(user_id),
        )

    await callback.message.delete()


@router.callback_query(F.data == "instruction")
async def instruction(callback: types.CallbackQuery):
    try:
        user_id = callback.from_user.id
        message_text = (
            f"Тут повинен бути текст."
            if db.get_user_language(user_id) == "ua"
            else f"Тут должен быть текст."
        )
        await callback.answer(message_text, show_alert=True)
        # await callback.message.edit_text(message_text, reply_markup=create_wallet_keyboard(user_id))
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            await callback.answer(f"", show_alert=True)
