from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
    Message,
    CallbackQuery,
    KeyboardButton,
    ReplyKeyboardMarkup,
    FSInputFile,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

import keyboards.inline as inl_kb
import data.user_data as db


router = Router()


def settings_menu_message(user_id):
    language = db.get_user_language(user_id)
    if language == "ua":
        return f"Оберіть опцію:"
    else:
        return f"Выберите опцию:"


def create_settings_menu_keyboard(user_id):
    language = db.get_user_language(user_id)
    builder = InlineKeyboardBuilder()
    if language == "ua":
        builder.button(
            text="Зміна мови інтерфейсу 🌍", callback_data="changing_language"
        )
        builder.button(text="Налаштування сповіщень 🔔", callback_data="f")
        builder.button(text="« Назад", callback_data="back_to_main_menu")
    else:
        builder.button(
            text="Изменение языка интерфейса 🌍", callback_data="changing_language"
        )
        builder.button(text="Настройки уведомлений 🔔", callback_data="f")
        builder.button(text="« Назад", callback_data="back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()


@router.callback_query(F.data == "settings")
async def settings_menu(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    message_text = settings_menu_message(user_id)
    language = db.get_user_language(user_id)

    if language == "ua":
        photo_path = FSInputFile("./data/images/settings_ua.JPG")
        await bot.send_photo(
            callback.from_user.id,
            photo=photo_path,
            caption=message_text,
            parse_mode="HTML",
            reply_markup=create_settings_menu_keyboard(user_id),
        )
    else:
        photo_path = FSInputFile("./data/images/settings_ru.JPG")
        await bot.send_photo(
            callback.from_user.id,
            photo=photo_path,
            caption=message_text,
            parse_mode="HTML",
            reply_markup=create_settings_menu_keyboard(user_id),
        )

    await callback.message.delete()


def create_language_keyboard2():
    languages = [
        ("Україньска", "ua"),
        ("Русский", "ru"),
    ]
    buttons = [
        [
            InlineKeyboardButton(text=label, callback_data=f"set_lang:{code}")
            for label, code in languages
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@router.callback_query(F.data == "changing_language")
async def set_language_command(callback: CallbackQuery):
    user_id = callback.from_user.id
    language = db.get_user_language(user_id)
    if language == "ua":
        await callback.message.answer(
            "Будь ласка, виберіть мову:", reply_markup=inl_kb.create_language_keyboard()
        )
    else:
        await callback.message.answer(
            "Пожалуйста, выберите язык:", reply_markup=inl_kb.create_language_keyboard()
        )
    await callback.message.delete()


@router.callback_query(F.data.startswith("set_lang"))
async def process_language_selection(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    language_code = callback.data.split(":")[1]

    db.set_user_language(user_id, language_code)
    language = db.get_user_language(user_id)

    if language == "ua":

        message_text = f"Вашу мову було змінено на ({language_code}) Україньска."

        photo_path = FSInputFile("./data/images/settings_ua.JPG")
        await bot.send_photo(
            callback.from_user.id,
            photo=photo_path,
            caption=message_text,
            parse_mode="HTML",
            reply_markup=create_settings_menu_keyboard(user_id),
        )

        await callback.message.delete()
    else:
        message_text = f"Ваш язык был изменен на ({language_code}) Русский."

        photo_path = FSInputFile("./data/images/settings_ru.JPG")
        await bot.send_photo(
            callback.from_user.id,
            photo=photo_path,
            caption=message_text,
            parse_mode="HTML",
            reply_markup=create_settings_menu_keyboard(user_id),
        )

        await callback.message.delete()


"""
-
-
-
"""


def support_menu_message(user_id):
    language = db.get_user_language(user_id)
    if language == "en":
        return (
            f"<b>Support 🔧</b>"
            f"\n\n"
            f"Our specialists are ready to answer any of your questions and help resolve any issues. Please contact us through the bot @DuskAirdropSupport, and we will get back to you as soon as possible!"
            f"\n\n"
            f"Support for the bot is available from 6:00 AM to 11:00 PM UTC."
            f"\n\n"
            f"🙏🏻 Please keep this in mind when reaching out."
        )
    else:
        return (
            f"<b>Поддержка 🔧</b>"
            f"\n\n"
            f"Наши специалисты готовы ответить на любые ваши вопросы и помочь в решении возникших проблем, напишите нам через бота @DuskAirdropSupport, и мы ответим вам в ближайшее время!"
            f"\n\n"
            f"Поддержка бота доступна с 6:00 до 23:00 по UTC."
            f"\n\n"
            f"🙏🏻 Пожалуйста, учитывайте это при обращении."
        )


@router.message(F.text.regexp(r"(?i)поддержка"))
@router.message(F.text.regexp(r"(?i)support"))
async def support_menu(message: Message):
    user_id = message.from_user.id
    text = support_menu_message(user_id)
    await message.answer(text, reply_markup=create_settings_menu_keyboard(user_id))
