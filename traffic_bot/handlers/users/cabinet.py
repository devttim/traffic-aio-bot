from datetime import timedelta, datetime

import aiohttp
from aiogram import Router, types, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup

import data.user_data as db
import keyboards.inline as inl_kb
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

exchange_rates = {"usd_to_uah": None, "uah_to_usd": None, "last_updated": None}


async def update_exchange_rates():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "tether", "vs_currencies": "uah"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()
                usd_to_uah = data["tether"]["uah"]
                uah_to_usd = round(1 / usd_to_uah, 6)  # Обратный курс

                exchange_rates.update(
                    {
                        "usd_to_uah": usd_to_uah,
                        "uah_to_usd": uah_to_usd,
                        "last_updated": datetime.now(),
                    }
                )
                print("Курсы обновлены:", exchange_rates)
    except Exception as e:
        print(f"Ошибка при обновлении курсов: {e}")


async def get_exchange_rates():
    last_updated = exchange_rates.get(
        "last_updated"
    )

    if last_updated is None or datetime.now() - last_updated > timedelta(minutes=10):
        await update_exchange_rates()

    return exchange_rates


@router.callback_query(F.data == "cabinet")
async def handler_offers(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    language = db.get_user_language(callback.from_user.id)
    status = db.get_user_status(callback.from_user.id)
    balance = await db.get_user_balance(user_id)
    if language == "ua":
        message_text = (
            f"Твій ID: {user_id}"
            f"\n"
            f"Баланс: {balance}"
            f"\n"
            f"Дохід: 0"
            f"\n"
            f"Cтатус: {status}"
            f"\n"
            f"Реквізити: Ви ще не додали жодного способу виплати."
        )

        photo_path = FSInputFile("./data/images/cab_ua.JPG")
        await bot.send_photo(
            callback.from_user.id,
            photo=photo_path,
            caption=message_text,
            parse_mode="HTML",
            reply_markup=inl_kb.keyboard_cabinet(user_id),
        )
    else:
        message_text = (
            f"Твой ID: {user_id}"
            f"\n"
            f"Баланс: {balance}"
            f"\n"
            f"Доход: 0"
            f"\n"
            f"Cтатус: {status}"
            f"\n"
            f"Реквизиты: Вы еще не добавили ни одного способа выплаты."
        )
        photo_path = FSInputFile("./data/images/cab_ru.JPG")
        await bot.send_photo(
            callback.from_user.id,
            photo=photo_path,
            caption=message_text,
            parse_mode="HTML",
            reply_markup=inl_kb.keyboard_cabinet(user_id),
        )
    await callback.message.delete()


@router.callback_query(F.data == "bind_details")
async def bind_details(callback: types.CallbackQuery):

    user_id = callback.from_user.id
    detail = db.get_detail_type(user_id)

    if detail == "None":
        try:
            message_text = (
                f"Виберіть тип гаманця, який бажаєте закріпити."
                if db.get_user_language(user_id) == "ua"
                else f"Выберите тип кошелька, который желаете закрепить."
            )
            await callback.message.answer(
                message_text, reply_markup=confirm_details_keyboard(user_id)
            )
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                await callback.answer(f"", show_alert=True)
    else:
        message_text = (
            f"Ви впевнені, що хочете змінити тип гаманця? Ваш попередній гаманець буде видалено."
            if db.get_user_language(user_id) == "ua"
            else f"Вы уверены, что хотите сменить тип кошелька? Ваш предыдущий кошелек будет удалён."
        )
        await callback.message.answer(
            message_text, reply_markup=confirm_details_keyboard(user_id)
        )

    await callback.message.delete()


def details_keyboard(user_id):
    language = db.get_user_language(user_id)
    builder = InlineKeyboardBuilder()
    if language == "ua":
        builder.button(text="Криптовалюта", callback_data="")
        builder.button(text="Банкiвська карта", callback_data="")
        builder.button(text="« Назад", callback_data="")
    else:
        builder.button(text="Криптовалюта", callback_data="")
        builder.button(text="Банковская карта", callback_data="")
        builder.button(text="« Назад", callback_data="")
    builder.adjust(1)
    return builder.as_markup()


@router.callback_query(F.data == "confirm_bind")
async def confirm_bind_details(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    user_detail = db.get_detail_type(user_id)

    if user_detail == "None":
        try:
            message_text = (
                f"Виберіть тип гаманця, який бажаєте закріпити."
                if db.get_user_language(user_id) == "ua"
                else f"Выберите тип кошелька, который желаете закрепить."
            )
            await callback.message.answer(
                message_text, reply_markup=details_keyboard(user_id)
            )
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                await callback.answer(f"", show_alert=True)
    else:
        message_text = (
            f"Виберіть тип гаманця, який бажаєте закріпити.\n\n⚠️ Ваш попередній гаманець буде видалено."
            if db.get_user_language(user_id) == "ua"
            else f"Выберите тип кошелька, который желаете закрепить.\n\n⚠️ Ваш предыдущий кошелек будет удалён."
        )
        await callback.message.answer(
            message_text, reply_markup=details_keyboard(user_id)
        )

    await callback.message.delete()


def confirm_details_keyboard(user_id):
    language = db.get_user_language(user_id)
    builder = InlineKeyboardBuilder()
    if language == "ua":
        builder.button(text="Так", callback_data="confirm_bind")
        builder.button(text="« Назад", callback_data="bind_details")
    else:
        builder.button(text="Да", callback_data="confirm_bind")
        builder.button(text="« Назад", callback_data="bind_details")
    builder.adjust(1)
    return builder.as_markup()


@router.callback_query(F.data == "confirm_bind")
async def confirm_bind_details(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    await callback.message.delete()


@router.callback_query(F.data == "output_request")
async def transaction_history(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    balance = db.get_user_balance(user_id)

    if balance >= 10:
        try:
            message_text = (
                f"Обсудить: Как будет происходить вывод, ручной?"
                if db.get_user_language(user_id) == "ua"
                else f"Обсудить: Как будет происходить вывод, ручной?"
            )
            await callback.answer(message_text, show_alert=True)
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                await callback.answer(f"", show_alert=True)
    else:
        message_text = (
            f"Виведення коштів доступне від $10."
            if db.get_user_language(user_id) == "ua"
            else f"Вывод средств доступен от $10."
        )
        await callback.answer(message_text, show_alert=True)
