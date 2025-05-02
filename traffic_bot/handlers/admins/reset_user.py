from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import admin_data as db

from keyboards.reply import admin_menu

from data.config import LOG_CHANNEL_ID, ADM_TID, ADMIN_USER_ID

from states.admins_states import DelStates

router = Router()


@router.message(F.text == "/delete_user", flags={"skip_logging": True})
async def ask_user_id_for_deletion(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_USER_ID:
        await message.answer("Введите ID пользователя, которого хотите удалить:")
        await state.set_state(DelStates.waiting_for_user_id)
    else:
        await message.reply("У вас нет доступа к этой команде.")


@router.message(DelStates.waiting_for_user_id)
async def confirm_user_deletion(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_USER_ID:
        user_id = message.text

        await state.update_data(user_id=user_id)

        kb = InlineKeyboardBuilder()
        kb.button(text="Подтвердить удаление", callback_data="confirm_deletion")
        kb.button(text="Отменить", callback_data="cancel_deletion")
        await message.answer(
            f"Вы уверены, что хотите удалить пользователя с ID: {user_id}?",
            reply_markup=kb.as_markup(),
        )

        await state.set_state(DelStates.waiting_for_confirmation)
    else:
        await message.reply("У вас нет доступа к этой команде.")


@router.callback_query(F.data == "confirm_deletion")
async def delete_user_confirmed(
    callback: types.CallbackQuery, state: FSMContext, bot: Bot
):
    data = await state.get_data()
    user_id = data.get("user_id")

    if user_id:
        db.delete_user_data(
            int(user_id)
        )
        await bot.send_message(
            callback.from_user.id, f"Данные пользователя с ID: {user_id} были удалены."
        )
    else:
        await bot.send_message(
            callback.from_user.id, "Ошибка: не удалось найти ID пользователя."
        )

    await state.clear()


@router.callback_query(F.data == "cancel_deletion")
async def cancel_user_deletion(
    callback: types.CallbackQuery, state: FSMContext, bot: Bot
):
    await bot.send_message(callback.from_user.id, "Удаление пользователя отменено.")
    await state.clear()
