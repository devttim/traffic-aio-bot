from aiogram import Router, types, F, Bot
import data.user_data as db
import keyboards.inline as inl_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

router = Router()


@router.callback_query(F.data == "offers")
async def handler_offers(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    language = db.get_user_language(callback.from_user.id)
    if language == "ua":
        message_text = f"Оберіть тематику для роботи:"

        photo_path = FSInputFile("./data/images/offer_ua.JPG")
        await bot.send_photo(
            callback.from_user.id,
            photo=photo_path,
            caption=message_text,
            parse_mode="HTML",
            reply_markup=inl_kb.keyboard_offers(user_id),
        )

    else:
        message_text = f"Выберите тематику для работы:"

        photo_path = FSInputFile("./data/images/offer_ru.JPG")
        await bot.send_photo(
            callback.from_user.id,
            photo=photo_path,
            caption=message_text,
            parse_mode="HTML",
            reply_markup=inl_kb.keyboard_offers(user_id),
        )

    await callback.message.delete()


async def handler_topic(callback: types.CallbackQuery):
    language = db.get_user_language(callback.from_user.id)
    if language == "ua":
        message_text = f"Поточні офери:"
        await callback.message.answer(message_text)
    else:
        message_text = f"Текущие офферы:"
        await callback.message.answer(message_text)
