import logging

from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    FSInputFile,
    BotCommand,
    MenuButtonCommands,
)

import data.user_data as db
import keyboards.inline as inl_kb
from data.config import PHOTO_START_URL, REWARD_PER_INVITE, LOG_CHANNEL_ID, CHANNEL_ID

from states.users_states import verification_request

router = Router()


def create_language_keyboard_start():
    languages = [
        ("Україньска", "ua"),
        ("Русский", "ru"),
    ]
    buttons = [
        [InlineKeyboardButton(text=label, callback_data=f"set_lang_start:{code}")]
        for label, code in languages
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@router.message(
    Command("start"), F.chat.type == "private", flags={"skip_logging": True}
)
async def start_handler(message: types.Message, bot: Bot):

    is_not_new_user = await db.user_exists(message.from_user.id)
    first_name = message.from_user.first_name
    user_id = message.from_user.id
    username = message.from_user.username
    start_command = message.text
    invited_by = start_command[7:]

    user_verified = db.get_user_verification_status(user_id)

    if is_not_new_user:
        if user_verified == "verified":

            photo_path = FSInputFile("./data/images/start.JPG")
            await bot.send_photo(
                chat_id=message.from_user.id,
                photo=photo_path,
                caption=start_message(first_name, user_id, username),
                parse_mode="HTML",
                reply_markup=inl_kb.user_menu(user_id),
            )

        else:
            keyboard = InlineKeyboardBuilder()
            keyboard.button(text="Пройти ✅", callback_data="verify")
            await message.answer(
                "Для начала пройдите верификацию, чтобы получить полный доступ к функционалу.",
                reply_markup=keyboard.as_markup(),
            )
    else:
        if invited_by:
            if invited_by != str(message.from_user.id):
                try:
                    await db.add_user(message.from_user.id, int(invited_by))
                    await db.update_reward_status(message.from_user.id, "not_received")

                    invited_by = await db.get_invited_by(message.from_user.id)
                    if invited_by:
                        pass

                except Exception as e:
                    await message.answer(
                        text=f"An error occurred: {e}.", show_alert=True
                    )
            else:
                await bot.send_message(
                    message.from_user.id,
                    "Регистрация по собственной реферальной ссылке запрещена!",
                )
        else:
            try:
                await db.add_user(message.from_user.id, 0)
            except Exception as e:
                logging.error(f"Error in start_handler: {e}")
                await message.answer(
                    "Произошла ошибка, попробуйте позже.", show_alert=True
                )

        message_text = f"Выберите язык/Оберіть мову:"
        await message.answer(
            message_text, reply_markup=create_language_keyboard_start()
        )


def start_message(first_name: str, user_id: int, username: str) -> str:
    language = db.get_user_language(user_id)
    if language == "ua":
        return (
            f"<b> Вітаю, @{username}!</b>\n\n"
            "Я Лінкач, адмін цієї крутої CPM-мережі, і мій вайб - з'єднувати найкращих з найкращими. 😎\n\n"
            "Моя мета - бути ніби Купідоном, але замість стріл у мене - соковиті офери! 🎯 Я обʼєднаю топ майстрів, які готові робити круту роботу, і VIP-замовників, які цінують якість та професіоналізм.\n\n"
            "Тут немає місця ботам та шахраям! Лише чесний трафік без накруток та мотиву. Все по-чесному та прозоро! 🤝\n\n"
            "Я обожнюю пряму рекламу в TG-каналах, Ads TG і TikTok - це моя стихія! 🚀\n\n"
            "Лінкач - це просто, вигідно та надійно. 🔥\n\n"
            "Якщо ти шукаєш круті офери або класних виконавців - приєднуйся до моєї команди! 👇"
        )
    else:
        return (
            f"<b> Привет, @{username}!</b>\n\n"
            "Я Линкач, админ этой крутой CPM-сети, и мой вайб - соединять лучших с лучшими. 😎\n\n"
            "Моя цель - быть как Купидон, но вместо стрел у меня - сочные офферы! 🎯 Я объединяю топ мастеров, которые готовы делать крутую работу, и VIP-заказчиков, которые ценят качество и профессионализм.\n\n"
            "Здесь нет места ботам и мошенникам! Только честный трафик без накруток и мотивов. Все честно и прозрачно! 🤝\n\n"
            "Я обожаю прямую рекламу в TG-каналах, Ads TG и TikTok - это моя стихия! 🚀\n\n"
            "Линкач - это просто, выгодно и надежно. 🔥\n\n"
            "Если ты ищешь крутые офферы или классных исполнителей - присоединяйся к моей команде! 👇"
        )


@router.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu(callback: types.callback_query, bot: Bot):
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name
    username = callback.from_user.username

    photo_path = FSInputFile("data/images/start.jpg")
    await bot.send_photo(
        callback.from_user.id,
        photo=photo_path,
        caption=start_message(first_name, user_id, username),
        parse_mode="HTML",
        reply_markup=inl_kb.user_menu(user_id),
    )
    await callback.message.delete()


@router.callback_query(F.data.startswith("set_lang_start"))
async def process_language_selection(
    callback: types.CallbackQuery, bot: Bot, state: FSMContext
):
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name
    username = callback.from_user.username
    language_code = callback.data.split(":")[1]  # Получаем код языка из текста

    db.set_user_language(user_id, language_code)
    language = db.get_user_language(user_id)

    user_verified = db.get_user_verification_status(user_id)

    if language == "ua":
        await callback.message.answer(
            f"Вашу мову було змінено на ({language_code}) Її можна завжди змінити в налаштуваннях у будь-який момент."
        )
        await callback.message.delete()
    else:
        await callback.message.answer(
            f"Ваш язык был изменен на ({language_code}) Её можно всегда изменить в настройках в любой момент."
        )
        await callback.message.delete()

    if user_verified == "verified":
        photo_path = FSInputFile("data/images/start.jpg")
        await bot.send_photo(
            callback.from_user.id,
            photo=photo_path,
            caption=start_message(first_name, user_id, username),
            parse_mode="HTML",
            reply_markup=inl_kb.user_menu(user_id),
        )
    else:
        if language == "ua":
            await callback.answer(
                f"Пройдіть верифікацію!\n"
                f"Відповідайте на кілька запитань, щоб подати заявку. Її розглянуть якнайшвидше!",
                show_alert=True,
            )

            await callback.message.answer(
                "1. Які джерела трафіку ви використовуєте для просування Telegram-каналів?\n\n"
                "2. Який час ви готові щоденно приділяти роботі з арбітражем трафіку?\n\n"
                "3. Опишіть ваш досвід роботи з арбітражем трафіку, зокрема:\n"
                "   - Найбільш успішні кейси.\n"
                "   - Ключові методи залучення цільової аудиторії, які ви використовуєте для телеграм-каналів.\n\n"
                "4. Які ваші конкурентні переваги порівняно з іншими фахівцями в цій галузі? Наведіть конкретні приклади унікальних навичок або ресурсів.\n\n"
                "5. Як ви плануєте професійний розвиток у сфері арбітражу трафіку? Назвіть інструменти, курси або практики, які використовуєте для вдосконалення.\n\n"
                "6. Опишіть ваш алгоритм дій у разі виникнення претензій від замовника щодо якості трафіку. Як ви забезпечуватимете прозору комунікацію та вирішення проблем?\n\n"
                "7. Як ви дізналися про нашу команду та що саме стало вирішальним фактором у вашому бажанні співпрацювати саме з нами?",
                show_alert=True,
            )
            await state.set_state(verification_request.waiting_for_answer)
        else:
            await callback.answer(
                f"Пройдите верификацию!\n"
                f"Ответье на несколько вопросов, чтобы подать заявку, её рассмотрят как можно скорее!",
                show_alert=True,
            )

            await callback.message.answer(
                "1. Какие источники трафика вы используете для продвижения Telegram-каналов?\n\n"
                "2. Сколько времени вы готовы ежедневно уделять работе с арбитражем трафика?\n\n"
                "3. Опишите ваш опыт работы с арбитражем трафика, в частности:\n"
                "   - Самые успешные кейсы.\n"
                "   - Ключевые методы привлечения целевой аудитории, которые вы используете для Telegram-каналов.\n\n"
                "4. В чем ваши конкурентные преимущества по сравнению с другими специалистами в этой сфере? Приведите конкретные примеры уникальных навыков или ресурсов.\n\n"
                "5. Как вы планируете профессиональное развитие в сфере арбитража трафика? Назовите инструменты, курсы или практики, которые используете для совершенствования.\n\n"
                "6. Опишите ваш алгоритм действий в случае претензий от заказчика по поводу качества трафика. Как вы обеспечите прозрачную коммуникацию и решение проблем?\n\n"
                "7. Как вы узнали о нашей команде, и что стало решающим фактором в вашем желании сотрудничать именно с нами?",
                show_alert=True,
            )
            await state.set_state(verification_request.waiting_for_answer)


@router.message(verification_request.waiting_for_answer)
async def save_answer(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✅ Отправить", callback_data="confirm_send")
    keyboard.button(text="🔄 Повторить", callback_data="repeat")
    keyboard.button(text="❌ Отмена", callback_data="cancel")

    await message.answer(
        "Ваш ответ записан. Отправить его на рассмотрение?",
        reply_markup=keyboard.as_markup(),
    )
    await state.set_state(verification_request.confirm_sending)


@router.callback_query(F.data == "confirm_send")
async def confirm_send(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    answer = data.get("answer")
    user_id = callback.from_user.id
    if answer:
        await bot.send_message(
            CHANNEL_ID,
            f"📝 Новый ответ от пользователя #{user_id}:\n\n{answer}",
            message_thread_id=2,
        )
        await callback.message.answer("✅ Ваш ответ успешно отправлен!")
    else:
        await callback.message.answer("⚠ Ошибка: нет данных для отправки.")

    await callback.message.delete()
    await state.clear()


@router.callback_query(F.data == "repeat")
async def repeat(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите ваш ответ заново:")
    await callback.message.delete()
    await state.set_state(verification_request.waiting_for_answer)


@router.callback_query(F.data == "cancel")
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("❌ Отменено.")
    await callback.message.delete()
    await state.clear()


@router.callback_query(F.data == "verify")
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    language = db.get_user_language(user_id)

    if language == "ua":
        await callback.answer(
            f"Пройдіть верифікацію!\n"
            f"Відповідайте на кілька запитань, щоб подати заявку. Її розглянуть якнайшвидше!",
            show_alert=True,
        )

        await callback.message.answer(
            "1. Які джерела трафіку ви використовуєте для просування Telegram-каналів?\n\n"
            "2. Який час ви готові щоденно приділяти роботі з арбітражем трафіку?\n\n"
            "3. Опишіть ваш досвід роботи з арбітражем трафіку, зокрема:\n"
            "   - Найбільш успішні кейси.\n"
            "   - Ключові методи залучення цільової аудиторії, які ви використовуєте для телеграм-каналів.\n\n"
            "4. Які ваші конкурентні переваги порівняно з іншими фахівцями в цій галузі? Наведіть конкретні приклади унікальних навичок або ресурсів.\n\n"
            "5. Як ви плануєте професійний розвиток у сфері арбітражу трафіку? Назвіть інструменти, курси або практики, які використовуєте для вдосконалення.\n\n"
            "6. Опишіть ваш алгоритм дій у разі виникнення претензій від замовника щодо якості трафіку. Як ви забезпечуватимете прозору комунікацію та вирішення проблем?\n\n"
            "7. Як ви дізналися про нашу команду та що саме стало вирішальним фактором у вашому бажанні співпрацювати саме з нами?",
            show_alert=True,
        )
        await state.set_state(verification_request.waiting_for_answer)
    else:
        await callback.answer(
            f"Пройдите верификацию!\n"
            f"Ответье на несколько вопросов, чтобы подать заявку, её рассмотрят как можно скорее!",
            show_alert=True,
        )

        await callback.message.answer(
            "1. Какие источники трафика вы используете для продвижения Telegram-каналов?\n\n"
            "2. Сколько времени вы готовы ежедневно уделять работе с арбитражем трафика?\n\n"
            "3. Опишите ваш опыт работы с арбитражем трафика, в частности:\n"
            "   - Самые успешные кейсы.\n"
            "   - Ключевые методы привлечения целевой аудитории, которые вы используете для Telegram-каналов.\n\n"
            "4. В чем ваши конкурентные преимущества по сравнению с другими специалистами в этой сфере? Приведите конкретные примеры уникальных навыков или ресурсов.\n\n"
            "5. Как вы планируете профессиональное развитие в сфере арбитража трафика? Назовите инструменты, курсы или практики, которые используете для совершенствования.\n\n"
            "6. Опишите ваш алгоритм действий в случае претензий от заказчика по поводу качества трафика. Как вы обеспечите прозрачную коммуникацию и решение проблем?\n\n"
            "7. Как вы узнали о нашей команде, и что стало решающим фактором в вашем желании сотрудничать именно с нами?",
            show_alert=True,
        )
        await state.set_state(verification_request.waiting_for_answer)

    await callback.message.delete()
