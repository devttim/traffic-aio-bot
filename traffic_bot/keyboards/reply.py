from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import data.user_data as db


def user_menu(user_id):

    language = db.get_user_language(user_id)
    if language == "ua":
        keyboard = [
            [types.KeyboardButton(text="Офери"), types.KeyboardButton(text="Кабінет")],
            [types.KeyboardButton(text="Партнерська програма")],
            [
                types.KeyboardButton(text="Ресурси"),
                types.KeyboardButton(text="Налаштування"),
            ],
        ]
    else:
        keyboard = [
            [types.KeyboardButton(text="Оферы"), types.KeyboardButton(text="Кабинет")],
            [types.KeyboardButton(text="Партнёрская программа")],
            [
                types.KeyboardButton(text="Ресурсы"),
                types.KeyboardButton(text="Настройки"),
            ],
        ]

    return types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)


def admin_menu():

    keyboard = [
        [
            types.KeyboardButton(text="Управление ОП"),
            types.KeyboardButton(text="Блокировать пользователя"),
        ],
        [
            types.KeyboardButton(text="Получить статистику"),
            types.KeyboardButton(text="Отправить рассылку"),
        ],
        [types.KeyboardButton(text="Управление балансами")],
    ]

    return types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)
