from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

from config import ADMIN_ID
from media import CATALOG_PHOTO_ID
from keyboards.inline import start_kb

router = Router()


@router.message(Command("menu"))
async def menu_handler(message: types.Message):
    is_admin = message.from_user.id == ADMIN_ID

    await message.answer_photo(
        photo=CATALOG_PHOTO_ID,
        caption=(
            "🍔 Добро пожаловать!\n\n"
            "Выберите действие:"
        ),
        reply_markup=start_kb(is_admin=is_admin)
    )

    try:
        await message.delete()
    except TelegramBadRequest:
        pass


@router.message(F.text)
async def fallback_handler(message: types.Message):
    is_admin = message.from_user.id == ADMIN_ID

    await message.answer_photo(
        photo=CATALOG_PHOTO_ID,
        caption=(
            "Я работаю через кнопки 👇\n\n"
            "Выберите действие:"
        ),
        reply_markup=start_kb(is_admin=is_admin)
    )

    try:
        await message.delete()
    except TelegramBadRequest:
        pass