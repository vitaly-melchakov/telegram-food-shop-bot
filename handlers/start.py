
from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.reply import main_menu
from keyboards.reply import keyboard
from config import ADMIN_ID
router = Router()

SHOP_NAME = "Burgers"

@router.message(CommandStart())
async def start(message:types.Message, state:FSMContext ):
    await state.clear()
    await state.update_data (cart = {})
    await message.answer ("Добро пожаловать в Burgers! 🍔", reply_markup=main_menu) 
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            "Вы вошли как администратор 👨‍💻\n\n"
            "Доступные команды:\n"
            "/orders — все заказы\n"
            "/orders_new — новые заказы\n"
            "/orders_done — выполненные заказы\n"
            "/orders_cancelled — отменённые заказы\n"
            "/admin_help — помощь по админ-панели"
        )

@router.message(F.text == "Главное меню")
async def menu(message:types.Message ):
   await message.answer ("Выберите товар в каталоге или посмотрите уже добавленные товары в корзине", reply_markup=keyboard)

   
