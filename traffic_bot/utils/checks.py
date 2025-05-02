from aiogram import Bot, types, F

from aiogram.utils.keyboard import InlineKeyboardBuilder

# from handlers.errors.error_handler import register_errors_handler
from data.config import API_TOKEN, LOG_CHANNEL_ID
from keyboards.reply import user_menu


from data import admin_data as db


async def check_subscribe(user_id, bot: Bot):
    channels = db.get_active_channels()

    for channel in channels:
        channel_name = channel[0]
        channel_id = channel[1]
        try:
            chat_member = await bot.get_chat_member(channel_id, user_id)
            if chat_member.status == "left":
                keyboard = InlineKeyboardBuilder()


                for name, _, link in channels:
                    keyboard.add(types.InlineKeyboardButton(text=name, url=link))

                keyboard.adjust(1)
                keyboard.add(
                    types.InlineKeyboardButton(
                        text="Проверить", callback_data="check_subscription"
                    )
                )

                await bot.send_message(
                    chat_id=user_id,
                    text="Вы должны подписаться на все каналы, чтобы использовать бота.",
                    reply_markup=keyboard.as_markup(),
                )
                return False
        except Exception as e:
            await bot.send_message(
                LOG_CHANNEL_ID,
                f"<b>Ошибка при проверке пользователя {user_id} на канале {channel_name} ({channel_id}):</b> {e}.",
            )
            continue
    return True
