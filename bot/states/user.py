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
    order_type = State()
    adress_input = State()
    time = State()
    payment_method = State()
    order_confirmation = State()
