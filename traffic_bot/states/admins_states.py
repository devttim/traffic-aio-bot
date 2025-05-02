from aiogram.fsm.state import State, StatesGroup


class DelStates(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_confirmation = State()


class VerifyStates(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_confirmation = State()


# Состояния для FSM
class AdminStates(StatesGroup):
    waiting_for_broadcast_message = State()
    waiting_for_user_range = State()
    waiting_for_confirmation = State()
    waiting_for_image = State()
    waiting_for_button = State()
