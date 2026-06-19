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
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ К списку заказов",
                    callback_data="admin_orders:all"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👨‍💻 Админ-панель",
                    callback_data="admin_panel"
                )
            ]
        ]
    )

    return keyboard



def admin_panel_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📦 Все заказы",
                    callback_data="admin_orders:all"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🆕 Новые",
                    callback_data="admin_orders:new"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Выполненные",
                    callback_data="admin_orders:done"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Отменённые",
                    callback_data="admin_orders:cancelled"
                )
            ],
                   [
            InlineKeyboardButton(
                text="🏠 Главное меню",
                callback_data="main_menu"
            )
            ]
        ]
    )


def admin_orders_back_kb(status: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Обновить",
                    callback_data=f"admin_orders:{status}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 В админ-панель",
                    callback_data="admin_panel"
                )
            ],
        ]
    )