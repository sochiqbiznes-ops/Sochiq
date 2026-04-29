from aiogram.fsm.state import State, StatesGroup

class CRMStates(StatesGroup):
    waiting_customer_name = State()
    waiting_take_count = State()
    waiting_pay_amount = State()
    waiting_price_value = State()