from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router




router = Router()



def admin_order_kb(order_id: int):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Выполнен",
                    callback_data=f"admin_done:{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Отменить",
                    callback_data=f"admin_cancel:{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Новый",
                    callback_data=f"admin_new:{order_id}"
                )
            ]
        ]
    )

    return keyboard