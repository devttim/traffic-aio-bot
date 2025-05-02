import asyncio
import os
import re
from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from data import admin_data as db
from keyboards.reply import admin_menu
from data.config import LOG_CHANNEL_ID, ADM_TID, ADMIN_USER_ID

router = Router()


@router.message(F.text == "Управление ОП", flags={"skip_logging": True})
async def show_admin_commands(message: types.Message):
    if message.from_user.id in ADMIN_USER_ID:
        message_func = (
            "<b>Доступные команды:</b>\n\n"
            "<code>/add_channel</code> (channel_id) (name) (link)\n"
            "▪️ Добавляет новый канал в базу данных.\n\n"
            "<code>/toggle_channel</code> (channel_id) (status)\n"
            "▪️ Обновляет статус канала (on для активации и off для деактивации).\n\n"
            "<code>/remove_channel</code> name\n"
            "▪️ Удаляет все каналы с указанным именем из базы данных.\n\n"
            "<code>/list_channels</code>\n"
            "▪️ Показывает список всех каналов."
        )
        await message.answer(message_func)
    else:
        await message.reply("У вас нет доступа к этой команде.")


@router.message(Command("add_channel"), flags={"skip_logging": True})
async def add_channel_command(message: types.Message, bot: Bot):
    if message.from_user.id in ADMIN_USER_ID:
        try:
            args = re.findall(r"\((.*?)\)", message.text)
            if len(args) != 3:
                await message.answer(
                    "Использование: /add_channel (channel_id) (name) (link)"
                )
                return

            channel_id, name, link = args
            db.add_channel(name, channel_id, link)
            await message.answer(f"Канал {name} был успешно добавлен.")
            await bot.send_message(
                LOG_CHANNEL_ID,
                f"Канал {name} был успешно добавлен.",
                message_thread_id=ADM_TID,
            )

        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
    else:
        await message.reply("У вас нет доступа к этой команде.")


@router.message(Command("toggle_channel"), flags={"skip_logging": True})
async def toggle_channel_command(message: types.Message, bot: Bot):
    if message.from_user.id in ADMIN_USER_ID:
        try:
            args = message.text.split()
            if len(args) != 3:
                await message.answer(
                    "Использование: /toggle_channel <channel_id> <status>"
                )
                return

            _, channel_id, status = args
            is_active = 1 if status.lower() == "on" else 0
            db.update_channel_status(channel_id, is_active)
            await message.answer(
                f"Статус канала {channel_id} был обновлен на {'активен' if is_active else 'неактивен'}."
            )
            await bot.send_message(
                LOG_CHANNEL_ID,
                f"Статус канала {channel_id} был обновлен на {'активен' if is_active else 'неактивен'}.",
                message_thread_id=ADM_TID,
            )

        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
    else:
        await message.reply("У вас нет доступа к этой команде.")


@router.message(Command("remove_channel"), flags={"skip_logging": True})
async def remove_channel_command(message: types.Message, bot: Bot):
    if message.from_user.id in ADMIN_USER_ID:
        try:
            args = message.text.split(maxsplit=1)
            if len(args) != 2:
                await message.answer("Использование: /remove_channel <name>")
                return

            _, name = args
            db.remove_channel_by_name(name)
            await message.answer(f"Все каналы с именем {name} были успешно удалены.")
            await bot.send_message(
                LOG_CHANNEL_ID,
                f"Все каналы с именем {name} были успешно удалены.",
                message_thread_id=ADM_TID,
            )
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
    else:
        await message.reply("У вас нет доступа к этой команде.")


@router.message(Command("list_channels"), flags={"skip_logging": True})
async def list_channels_command(message: types.Message):
    if message.from_user.id in ADMIN_USER_ID:
        try:
            channels = db.get_all_channels()
            if not channels:
                await message.answer("Каналов не найдено.")
            else:
                message_text = "\n".join(
                    [
                        f"Имя: {channel[0]}"
                        f"\n"
                        f"ID: <code>{channel[1]}</code>"
                        f"\n"
                        f"Ссылка: {channel[2]}"
                        f"\n"
                        f"Статус: {'активен' if channel[3] == 1 else 'неактивен'}"
                        f"\n"
                        for channel in channels
                    ]
                )
                await message.answer(message_text, disable_web_page_preview=True)
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
    else:
        await message.reply("У вас нет доступа к этой команде.")
