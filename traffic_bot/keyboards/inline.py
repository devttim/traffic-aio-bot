from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
import data.user_data as db
from aiogram.utils.keyboard import InlineKeyboardBuilder


def user_menu(user_id):
    language = db.get_user_language(user_id)
    if language == "ua":
        keyboard = [
            [
                types.InlineKeyboardButton(text="Офери", callback_data="offers"),
                types.InlineKeyboardButton(text="Кабінет", callback_data="cabinet"),
            ],
            [
                types.InlineKeyboardButton(
                    text="Партнерська програма", callback_data="affiliate"
                )
            ],
            [
                types.InlineKeyboardButton(text="Ресурси", callback_data="resources"),
                types.InlineKeyboardButton(
                    text="Налаштування", callback_data="settings"
                ),
            ],
        ]
    else:
        keyboard = [
            [
                types.InlineKeyboardButton(text="Оферы", callback_data="offers"),
                types.InlineKeyboardButton(text="Кабинет", callback_data="cabinet"),
            ],
            [
                types.InlineKeyboardButton(
                    text="Партнёрская программа", callback_data="affiliate"
                )
            ],
            [
                types.InlineKeyboardButton(text="Ресурсы", callback_data="resources"),
                types.InlineKeyboardButton(text="Настройки", callback_data="settings"),
            ],
        ]

    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)


def keyboard_offers(user_id):
    language = db.get_user_language(user_id)
    if language == "ua":
        keyboard = [
            [
                InlineKeyboardButton(text="Тема 1", callback_data="ff"),
                InlineKeyboardButton(text="Тема 2", callback_data="ff"),
            ],
            [
                InlineKeyboardButton(text="Тема 3", callback_data="ff"),
                InlineKeyboardButton(text="Тема 4", callback_data="ff"),
            ],
            [
                InlineKeyboardButton(text="Тема 5", callback_data="ff"),
                InlineKeyboardButton(text="Тема 6", callback_data="ff"),
            ],
            [InlineKeyboardButton(text="« Назад", callback_data="back_to_main_menu")],
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton(text="Тема 1", callback_data="f"),
                InlineKeyboardButton(text="Тема 2", callback_data="ff"),
            ],
            [
                InlineKeyboardButton(text="Тема 3", callback_data="ff"),
                InlineKeyboardButton(text="Тема 4", callback_data="ff"),
            ],
            [
                InlineKeyboardButton(text="Тема 5", callback_data="ff"),
                InlineKeyboardButton(text="Тема 6", callback_data="ff"),
            ],
            [InlineKeyboardButton(text="« Назад", callback_data="back_to_main_menu")],
        ]

    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)


def keyboard_resources(user_id):
    language = db.get_user_language(user_id)
    if language == "ua":
        keyboard = [
            [
                InlineKeyboardButton(
                    text="Канал сервісу 📱", url="https://t.me/+_pM8Sg1Xs1A0ZTM6"
                )
            ],
            [InlineKeyboardButton(text="Інструкція 📌", callback_data="instruction")],
            [
                InlineKeyboardButton(
                    text="Підтримка 💬", url="https://t.me/+_pM8Sg1Xs1A0ZTM6"
                )
            ],
            [InlineKeyboardButton(text="« Назад", callback_data="back_to_main_menu")],
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton(
                    text="Канал сервиса 📱", url="https://t.me/+_pM8Sg1Xs1A0ZTM6"
                )
            ],
            [InlineKeyboardButton(text="Инструкция 📌", callback_data="instruction")],
            [
                InlineKeyboardButton(
                    text="Поддержка 💬", url="https://t.me/+_pM8Sg1Xs1A0ZTM6"
                )
            ],
            [InlineKeyboardButton(text="« Назад", callback_data="back_to_main_menu")],
        ]

    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)


def _menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Тема 1", url=""),
                InlineKeyboardButton(text="", callback_data=""),
            ],
        ]
    )


def create_language_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Українська", callback_data="set_lang:ua")
    builder.button(text="Русский", callback_data="set_lang:ru")
    builder.adjust(1)
    return builder.as_markup()


def keyboard_cabinet(user_id):
    language = db.get_user_language(user_id)
    builder = InlineKeyboardBuilder()
    if language == "ua":
        builder.button(text="Прив'язати реквізити", callback_data="bind_details")
        builder.button(text="Запит на виплату", callback_data="output_request")
        builder.button(text="« Назад", callback_data="back_to_main_menu")
    else:
        builder.button(text="Привязать реквизиты", callback_data="bind_details")
        builder.button(text="Запрос вывода", callback_data="output_request")
        builder.button(text="« Назад", callback_data="back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()


def keyboard_back_main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="« Назад", callback_data="back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()
