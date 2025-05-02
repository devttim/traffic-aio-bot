# middleware/subscribe.py
import logging
from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.dispatcher.flags import get_flag


class SubscribeMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        from utils.checks import check_subscribe  # Ленивый импорт

        user = event.from_user

        # Проверка на наличие флага skip_logging
        if get_flag(data, "skip_logging"):
            return await handler(event, data)

        bot = data["bot"]
        is_subscribed = await check_subscribe(user.id, bot)

        if not is_subscribed:
            return

        if user:
            logging_context = (
                f"Handler: {handler.__name__}, User: {user.full_name} (ID: {user.id})"
            )
            logging.info(logging_context)

        return await handler(event, data)
