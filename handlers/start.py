
from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.inline import main_inline_kb
from config import ADMIN_ID
router = Router()

SHOP_NAME = "Burgers"

@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await state.update_data(cart={})

    await message.answer(
        "Добро пожаловать в Burgers! 🍔\n\n"
        "Нажмите кнопку ниже, чтобы открыть каталог.",
        reply_markup=main_inline_kb()
    )

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


@router.callback_query(F.data == "main:menu")
async def callback_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await state.update_data(cart={})

    text = (
        "Добро пожаловать в Burgers! 🍔\n\n"
        "Нажмите кнопку ниже, чтобы открыть каталог."
    )

    if callback.message.photo:
        await callback.message.delete()

        await callback.message.answer(
            text,
            reply_markup=main_inline_kb()
        )
    else:
        await callback.message.edit_text(
            text,
            reply_markup=main_inline_kb()
        )