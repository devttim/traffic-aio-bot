from aiogram import Router, types, F
from data import user_data as db
from data.config import LOG_CHANNEL_ID, ADM_TID, ADMIN_USER_ID

router = Router()


@router.message(F.text == "Получить статистику", flags={"skip_logging": True})
async def show_statistics(message: types.Message):
    if message.from_user.id in ADMIN_USER_ID:
        try:
            total_users, active_users, inactive_users = db.get_subscription_statistics()
            message_func = (
                f"<b>Статистика подписчиков:</b>\n"
                f"Всего подписчиков: {total_users}\n"
                f"Активные: {active_users}\n"
                f"Неактивные: {inactive_users}"
            )
            await message.answer(message_func, parse_mode="HTML")
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
    else:
        await message.reply("У вас нет доступа к этой команде.")
