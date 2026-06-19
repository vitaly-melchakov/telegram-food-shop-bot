from aiogram import Router, F

from database import get_orders, get_order_items, update_order_status, get_orders_by_status, get_order_by_id
from config import ADMIN_ID
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.types import CallbackQuery

from keyboards.admin_kb import admin_panel_kb, admin_order_kb

router = Router()



ORDER_STATUS_MAP = {
    "new": "🆕 новый",
    "done": "✅ выполнен",
    "cancelled": "❌ отменён",
}

def format_order_status(status):
    return ORDER_STATUS_MAP.get(status, status)

async def safe_edit_text(callback: CallbackQuery, text: str, reply_markup=None) -> bool:
    try:
        if callback.message.photo:
            await callback.message.edit_caption(
                caption=text,
                reply_markup=reply_markup
            )
        else:
            await callback.message.edit_text(
                text,
                reply_markup=reply_markup
            )

        return True

    except TelegramBadRequest as e:
        error_text = str(e)

        if "message is not modified" in error_text:
            await callback.answer("Без изменений")
            return False

        if "there is no text in the message to edit" in error_text:
            await callback.message.edit_caption(
                caption=text,
                reply_markup=reply_markup
            )
            return True

        raise





@router.callback_query(F.data.startswith("admin_orders:"))
async def admin_orders_handler(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Нет доступа", show_alert=True)
        return

    status = callback.data.split(":")[1]

    if status == "all":
        orders = get_orders(limit=10)
        title = "📦 Все заказы"

    elif status == "new":
        orders = get_orders_by_status("new", limit=10)
        title = "🆕 Новые заказы"

    elif status == "done":
        orders = get_orders_by_status("done", limit=10)
        title = "✅ Выполненные заказы"

    elif status == "cancelled":
        orders = get_orders_by_status("cancelled", limit=10)
        title = "❌ Отменённые заказы"

    else:
        await callback.answer("Неизвестный фильтр", show_alert=True)
        return

    if not orders:
        await safe_edit_text(
            callback,
            f"{title}\n\nЗаказов пока нет.",
            reply_markup=admin_panel_kb()
        )

        await callback.answer()
        return

    text = (
        f"{title}\n\n"
        "Показаны последние 10 заказов.\n"
        "Выберите заказ:"
    )

    await safe_edit_text(
        callback,
        text,
        reply_markup=admin_orders_list_kb(orders)
    )

    await callback.answer()




def admin_orders_list_kb(orders):
    builder = InlineKeyboardBuilder()

    for order in orders:
        order_id = order[0]
        total_price = order[4]
        order_status = format_order_status(order[5])

        builder.button(
            text=f"📦 Заказ №{order_id} — {total_price} дин. — {order_status}",
            callback_data=f"admin_order:{order_id}"
        )

    builder.button(
        text="👨‍💻 Админ-панель",
        callback_data="admin_panel"
    )

    builder.adjust(1)
    return builder.as_markup()

@router.callback_query(F.data == "admin_panel")
async def admin_panel_handler(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Нет доступа", show_alert=True)
        return

    text = (
        "👨‍💻 Админ-панель\n\n"
        "Выберите, какие заказы показать:"
    )

    if callback.message.photo:
        await callback.message.edit_caption(
            caption=text,
            reply_markup=admin_panel_kb()
        )
    else:
        await callback.message.edit_text(
            text,
            reply_markup=admin_panel_kb()
        )

    await callback.answer()

@router.callback_query(F.data.startswith("admin_done:"))
async def admin_done_handler(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Нет доступа", show_alert=True)
        return

    order_id = int(callback.data.split(":")[1])

    update_order_status(order_id, "done")

    changed = await show_admin_order_card(callback, order_id)

    if changed:
        await callback.answer("Статус изменён")


@router.callback_query(F.data.startswith("admin_cancel:"))
async def admin_cancel_handler(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Нет доступа", show_alert=True)
        return

    order_id = int(callback.data.split(":")[1])

    update_order_status(order_id, "cancelled")

    changed = await show_admin_order_card(callback, order_id)

    if changed:
        await callback.answer("Статус изменён")


@router.callback_query(F.data.startswith("admin_new:"))
async def admin_new_handler(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Нет доступа", show_alert=True)
        return

    order_id = int(callback.data.split(":")[1])

    update_order_status(order_id, "new")

    changed = await show_admin_order_card(callback, order_id)

    if changed:
        await callback.answer("Статус изменён")


async def show_admin_order_card(callback: CallbackQuery, order_id: int) -> bool:
    order = get_order_by_id(order_id)

    if not order:
        await callback.answer("Заказ не найден", show_alert=True)
        return False

    items = get_order_items(order_id)

    order_id = order[0]
    full_name = order[1]
    username = order[2]
    user_id = order[3]
    total_price = order[4]
    status = order[5]
    created_at = order[6]

    username_text = f"@{username}" if username else "не указан"

    text = (
        f"📦 Заказ №{order_id}\n\n"
        f"Клиент: {full_name}\n"
        f"🔗 Username: {username_text}\n"
        f"User ID: {user_id}\n\n"
        f"Заказ:\n"
    )

    for item in items:
        product_name = item[0]
        quantity = item[1]
        price = item[2]

        text += f"• {product_name} x{quantity} — {price * quantity} дин.\n"

    text += (
        f"\nИтого: {total_price} дин.\n"
        f"Статус: {format_order_status(status)}\n"
        f"Дата: {created_at}"
    )

    changed = await safe_edit_text(
        callback,
        text,
        reply_markup=admin_order_kb(order_id)
    )

    return changed

@router.callback_query(F.data.startswith("admin_order:"))
async def admin_order_card_handler(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Нет доступа", show_alert=True)
        return

    order_id = int(callback.data.split(":")[1])

    changed = await show_admin_order_card(callback, order_id)

    if changed:
        await callback.answer()