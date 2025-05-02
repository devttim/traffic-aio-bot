import aiohttp
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

import random
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

import data.user_data as db
from data.config import BOT_USERNAME, REWARD_PER_INVITE
import keyboards.inline as inl_kb

router = Router()


@router.callback_query(F.data == "affiliate")
async def send_dusk_info(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id

    language = db.get_user_language(user_id)
    verified_invites = await db.get_invite_data(user_id)
    earned_reward = verified_invites * REWARD_PER_INVITE

    if language == "ua":
        message_text = (
            f"👥 <b>У цьому розділі ви можете побачити кількість запрошених партнерів через ваше реферальне посилання. </b>"
            f"\n\n"
            f"Запрошено: {verified_invites} користувачів"
            f"\n"
            f"Отримано винагороду: {earned_reward}"
            f"\n\n"
            f"<b>Ваша реферальна посилання:</b>"
            f"\n"
            f"<code>https://t.me/{BOT_USERNAME}?start={user_id}</code>"
            f"\n\n"
            f"<b>Ваш заробіток формується з відсотка від доходу рефералів.</b>"
        )

        photo_path = FSInputFile("./data/images/partner_ua.JPG")
        await bot.send_photo(
            callback.from_user.id,
            photo=photo_path,
            caption=message_text,
            parse_mode="HTML",
            reply_markup=inl_kb.keyboard_back_main_menu(),
        )
    else:
        message_text = (
            f"👥 В этом разделе вы можете увидеть количество приглашенных партнеров через вашу реферальную ссылку. "
            f"\n\n"
            f"Вы пригласили: {verified_invites} пользователей"
            f"\n"
            f"Полученное вознаграждение: {earned_reward}"
            f"\n\n"
            f"<b>Ваша пригласительная ссылка:</b>"
            f"\n"
            f"<code>https://t.me/{BOT_USERNAME}?start={user_id}</code>"
            f"\n\n"
            f"<b>Ваш заработок формируется из процента от дохода рефералов.</b>"
        )

        photo_path = FSInputFile("./data/images/partner_ru.JPG")
        await bot.send_photo(
            callback.from_user.id,
            photo=photo_path,
            caption=message_text,
            parse_mode="HTML",
            reply_markup=inl_kb.keyboard_back_main_menu(),
        )

    await callback.message.delete()
