from aiogram import Router, types, F
from aiogram.filters import Command
from database import get_orders, get_order_items, update_order_status, get_orders_by_status
from keyboards.inline import admin_order_kb
from config import ADMIN_ID

router = Router()



def build_orders_text(orders):
    status_names = {
        "new": "🆕 новый",
        "done": "✅ выполнен",
        "cancelled": "❌ отменён"
    }

    text = ""

    for order in orders:
        order_id = order[0]
        username = order[2]
        full_name = order[3]
        total_price = order[4]
        created_at = order[5]
        status = order[6]

        text += (
            f"🧾 Заказ #{order_id}\n"
            f"👤 Клиент: {full_name}\n"
            f"🔗 Username: @{username}\n"
            f"💰 Сумма: {total_price} дин\n"
            f"🕒 Дата: {created_at}\n"
            f"📌 Статус: {status_names.get(status, status)}\n\n"
            f"Товары:\n"
        )

        items = get_order_items(order_id)

        for item in items:
            product_name = item[0]
            quantity = item[1]
            price = item[2]

            item_total = quantity * price

            text += f"• {product_name} x{quantity} — {item_total} дин\n"

        text += "\n" + "—" * 20 + "\n\n"

    return text



@router.message(Command("orders"))
async def cmd_orders(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У тебя нет доступа к этой команде.")
        return

    orders = get_orders(10)

    if not orders:
        await message.answer("Заказов пока нет.")
        return

    text = "📦 Последние заказы:\n\n"
    text += build_orders_text(orders)



    await message.answer(text)


@router.message(Command("order_done"))
async def cmd_order_done(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У тебя нет доступа к этой команде.")
        return
  

    parts = message.text.split()

    if len(parts) != 2: 
        await message.answer( "Используй команду так:\n"
        "/order_done НОМЕР_ЗАКАЗА\n\n"
        "Например:\n"
        "/order_done 3")
        return

    order_id = parts[1]

    if not order_id.isdigit():
        await message.answer("ID заказа должен быть числом.")
        return

    update_order_status(int(order_id), "done")

    await message.answer(f"Заказ #{order_id} отмечен как выполненный ✅")

@router.message(Command("order_new"))   
async def cmd_order_new(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У тебя нет доступа к этой команде.")
        return

    parts = message.text.split()

    if len(parts) != 2:
        await message.answer(
            "Используй команду так:\n"
            "/order_new НОМЕР_ЗАКАЗА\n\n"
            "Например:\n"
            "/order_new 3"
        )
        return

    order_id = parts[1]

    if not order_id.isdigit():
        await message.answer("ID заказа должен быть числом.")
        return

    update_order_status(int(order_id), "new")

    await message.answer(f"Заказ #{order_id} снова отмечен как новый 🔄")



  
@router.message(Command("order_cancel"))  
async def cmd_order_cancel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У тебя нет доступа к этой команде.")
        return

    parts = message.text.split()

    if len(parts) != 2:
        await message.answer(
            "Используй команду так:\n"
            "/order_cancel НОМЕР_ЗАКАЗА\n\n"
            "Например:\n"
            "/order_cancel 3"
        )
        return

    order_id = parts[1]

    if not order_id.isdigit():
        await message.answer("ID заказа должен быть числом.")
        return

    update_order_status(int(order_id), "cancelled")

    await message.answer(f"Заказ #{order_id} отменён ❌")


@router.message(Command("orders_new"))
async def cmd_orders_new(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У тебя нет доступа к этой команде.")
        return

    orders = get_orders_by_status("new", 10)

    if not orders:
        await message.answer("Новых заказов пока нет.")
        return

    
    text = "🆕 Новые заказы:\n\n"
    text += build_orders_text(orders)


    await message.answer(text)

def update_admin_order_text(text: str, status_text: str):   
    if "\n\nСтатус:" in text:
        text = text.split("\n\nСтатус:")[0]

    return f"{text}\n\nСтатус: {status_text}"


@router.message(Command("orders_done"))
async def cmd_orders_done(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У тебя нет доступа к этой команде.")
        return

    orders = get_orders_by_status("done", 10)

    if not orders:
        await message.answer("Выполненных заказов пока нет.")
        return


    text = "✅ Выполненные заказы:\n\n"
    text += build_orders_text(orders)


   
    await message.answer(text)




@router.message(Command("orders_cancelled"))
async def cmd_orders_cancelled(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У тебя нет доступа к этой команде.")
        return

    orders = get_orders_by_status("cancelled", 10)

    if not orders:
        await message.answer("Отменённых заказов пока нет.")
        return


    text = "❌ Отменённые заказы:\n\n"
    text += build_orders_text(orders)


    await message.answer(text)


@router.message(Command("admin_help"))
async def cmd_admin_help(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У тебя нет доступа к этой команде.")
        return

    text = (
        "⚙️ Админ-команды:\n\n"
        "📦 /orders — показать последние заказы\n"
        "🆕 /orders_new — показать новые заказы\n"
        "✅ /orders_done — показать выполненные заказы\n"
        "❌ /orders_cancelled — показать отменённые заказы\n\n"
        "✅ /order_done ID — отметить заказ выполненным\n"
        "🔄 /order_new ID — вернуть заказ в новые\n"
        "❌ /order_cancel ID — отменить заказ\n\n"
        "Пример:\n"
        "/order_done 12"
    )

    await message.answer(text)


@router.callback_query(F.data.startswith("admin_done:"))
async def callback_admin_done(callback: types.CallbackQuery):
    order_id = int(callback.data.split(":")[1])

    if callback.from_user.id != ADMIN_ID:
        await callback.answer("У вас нет доступа", show_alert=True)
        return

    update_order_status(order_id, "done")

    new_text = update_admin_order_text(
        callback.message.text,
        "✅ выполнен"
    )

    await callback.message.edit_text(
        new_text,
        reply_markup=admin_order_kb(order_id)
    )

    await callback.answer("Заказ отмечен как выполненный ✅")

@router.callback_query(F.data.startswith("admin_cancel:"))
async def callback_admin_cancel(callback: types.CallbackQuery):
    order_id = int(callback.data.split(":")[1])

    if callback.from_user.id != ADMIN_ID:
        await callback.answer("У вас нет доступа", show_alert=True)
        return

    update_order_status(order_id, "cancelled")

    new_text = update_admin_order_text(
        callback.message.text,
        "❌ отменён"
    )

    await callback.message.edit_text(
        new_text,
        reply_markup=admin_order_kb(order_id)
    )

    await callback.answer("Заказ отменён ❌")


@router.callback_query(F.data.startswith("admin_new:"))
async def callback_admin_new(callback: types.CallbackQuery):
    order_id = int(callback.data.split(":")[1])

    if callback.from_user.id != ADMIN_ID:
        await callback.answer("У вас нет доступа", show_alert=True)
        return

    update_order_status(order_id, "new")

    new_text = update_admin_order_text(
        callback.message.text,
        "🆕 новый"
    )

    await callback.message.edit_text(
        new_text,
        reply_markup=admin_order_kb(order_id)
    )

    await callback.answer("Заказ снова отмечен как новый 🔄")