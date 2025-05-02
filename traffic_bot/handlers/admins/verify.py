from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import admin_data as db

from keyboards.reply import admin_menu

from data.config import LOG_CHANNEL_ID, ADM_TID, ADMIN_USER_ID

from states.admins_states import VerifyStates


router = Router()


@router.message(F.text == "/verify_user", flags={"skip_logging": True})
async def ask_user_id_for_deletion(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_USER_ID:
        await message.answer("Введите ID пользователя, которого хотите верефицировать:")
        await state.set_state(VerifyStates.waiting_for_user_id)
    else:
        await message.reply("У вас нет доступа к этой команде.")

@router.message(VerifyStates.waiting_for_user_id)
async def confirm_user_deletion(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_USER_ID:
        user_id = message.text

        # Сохраняем user_id в данные состояния
        await state.update_data(user_id=user_id)

        # Создаем клавиатуру с кнопками подтверждения и отмены
        kb = InlineKeyboardBuilder()
        kb.button(text="Подтвердить верификацию", callback_data="confirm_verify")
        kb.button(text="Отменить", callback_data="cancel_verify")
        await message.answer(
            f"Вы уверены, что хотите верифицировать пользователя с ID: {user_id}?",
            reply_markup=kb.as_markup(),
        )

        await state.set_state(VerifyStates.waiting_for_confirmation)
    else:
        await message.reply("У вас нет доступа к этой команде.")


@router.callback_query(F.data == "confirm_verify")
async def delete_user_confirmed(
    callback: types.CallbackQuery, state: FSMContext, bot: Bot
):
    data = await state.get_data()
    user_id = data.get("user_id")

    if user_id:
        await db.update_verification_status(int(user_id), "verified")
        await bot.send_message(
            callback.from_user.id, f"Пользователя с ID: {user_id} был верефицирован."
        )
    else:
        await bot.send_message(
            callback.from_user.id, "Ошибка: не удалось найти ID пользователя."
        )
    await callback.answer("")
    await state.clear()


@router.callback_query(F.data == "cancel_verify")
async def cancel_user_deletion(
    callback: types.CallbackQuery, state: FSMContext, bot: Bot
):
    await bot.send_message(callback.from_user.id, "Верификация пользователя отменена.")
    await state.clear()
