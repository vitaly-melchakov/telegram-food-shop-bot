from aiogram.fsm.state import StatesGroup, State
from aiogram import Router



router = Router()

class Shop (StatesGroup):
    catalog = State()
    cart = State()
    confirming = State()

