"""
FSM states
"""
from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    """User FSM states"""
    start = State()
    phone_number = State()
    menu = State()
    product_selection = State()
    would_image = State()
    waiting_for_image = State()
    first_name = State()
    last_name = State()
    time = State()
    order_confirmation = State()
