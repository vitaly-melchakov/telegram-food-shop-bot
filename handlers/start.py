
from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline import main_inline_kb
from config import ADMIN_ID

from aiogram.exceptions import TelegramBadRequest

router = Router()

SHOP_NAME = "Burgers"

from config import ADMIN_ID

def start_kb(is_admin: bool = False):
    buttons = [
        [
            InlineKeyboardButton(
                text="🍔 Открыть каталог",
                callback_data="open_catalog"
            )
        ]
    ]

    if is_admin:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="👨‍💻 Админ-панель",
                    callback_data="admin_panel"
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)



@router.message(CommandStart())
async def start_handler(message: Message):
    is_admin = message.from_user.id == ADMIN_ID

    await message.answer(
        "🍔 Добро пожаловать!\n\nВыберите действие:",
        reply_markup=start_kb(is_admin=is_admin)
    )

    try:
        await message.delete()
    except TelegramBadRequest:
        pass



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

