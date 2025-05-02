from aiogram.fsm.state import State, StatesGroup


# start
class verification_request(StatesGroup):
    waiting_for_answer = State()
    confirm_sending = State()
