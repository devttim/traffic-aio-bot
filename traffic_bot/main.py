import asyncio
import logging
from colorama import Fore, Style

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.formatting import BotCommand


from utils.checks import check_subscribe
from data.config import API_TOKEN
from keyboards.reply import user_menu
from handlers.users import offers, start, cabinet, resources, settings, affiliate
from handlers.admins import ban, input, mailing, op, reset_user, stats, verify

from middleware.subscribe import SubscribeMiddleware


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())

router = Router()


@router.callback_query(F.data == "check_subscription", flags={"skip_logging": True})
async def check_subscription_handler(callback_query: types.CallbackQuery, bot: Bot):
    user_id = callback_query.from_user.id

    is_subscribed = await check_subscribe(user_id, bot)

    if is_subscribed:
        await callback_query.message.edit_text(
            "Спасибо за подписку! Теперь вы можете пользоваться ботом.",
            reply_markup=user_menu(user_id),
        )
    else:
        await callback_query.answer(
            "Пожалуйста, подпишитесь на все каналы и попробуйте снова.", show_alert=True
        )
        await callback_query.message.delete()


router.include_router(cabinet.router)
router.include_router(offers.router)
router.include_router(start.router)
router.include_router(settings.router)
router.include_router(resources.router)
router.include_router(affiliate.router)

router.include_router(ban.router)
router.include_router(input.router)
router.include_router(mailing.router)
router.include_router(op.router)
router.include_router(reset_user.router)
router.include_router(stats.router)
router.include_router(verify.router)

router.message.middleware(SubscribeMiddleware())
router.callback_query.middleware(SubscribeMiddleware())

# Регистрация обработчика ошибок
# register_errors_handler(dp)

dp.include_router(router)

from aiogram.types import BotCommand


async def main():
    await dp.start_polling(bot)

    await bot.set_my_commands(
        [
            BotCommand(command="/start", description="Начать работу"),
        ]
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.GREEN}Bot Stopped. {Fore.BLUE}Бот выключен!{Style.RESET_ALL}")
