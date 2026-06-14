from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F

from keyboards.inline import admin_order_kb, order_success_kb, cart_inline_kb

from datetime import datetime

from config import ADMIN_ID

from database import get_product_by_id, save_order

from aiogram.types import InputMediaPhoto

from media import ORDER_SUCCESS_PHOTO_ID


router = Router()
time = datetime.now()
formatted_date = time.strftime("%d-%m-%y %H:%M")

order_number = 0



def get_order_success_image():
     return ORDER_SUCCESS_PHOTO_ID

@router.callback_query(F.data == "order:confirm")
async def callback_confirm_order(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cart = data.get("cart", {})

    if not cart:
        await callback.message.edit_caption(
            caption="🛒 Корзина пустая.",
            reply_markup=cart_inline_kb()
        )
        await callback.answer("Корзина пустая")
        return

    order_items_text = ""
    total = 0

    for product_id, quantity in cart.items():
        product = get_product_by_id(product_id)

        if product is None:
            continue

        name = product[1]
        price = product[2]

        subtotal = price * quantity
        total += subtotal

        order_items_text += f"{name} x{quantity} — {subtotal} дин\n"

    user = callback.from_user

    order_id = save_order(
        user_id=user.id,
        username=user.username,
        full_name=user.full_name,
        cart=cart
    )

    username_text = f"@{user.username}" if user.username else "не указан"

    admin_text = (
        f"🆕 Новый заказ №{order_id}!\n\n"
        f"Клиент: {user.full_name}\n"
        f"Username: {username_text}\n"
        f"User ID: {user.id}\n\n"
        f"Заказ:\n"
        f"{order_items_text}\n"
        f"Итого: {total} дин\n\n"
    )

    await callback.bot.send_message(
        ADMIN_ID,
        admin_text,
        reply_markup=admin_order_kb(order_id)
    )

    success_text = (f"✅ Заказ №{order_id}"
)
    
    if callback.message.photo:
      media = InputMediaPhoto(
        media=get_order_success_image(),
        caption=success_text
    )

      await callback.message.edit_media(
        media=media,
        reply_markup=order_success_kb()
    )
    else:
     await callback.message.edit_text(
        text=success_text,
        reply_markup=order_success_kb()
    )

    await state.clear()

    await callback.answer("Заказ подтверждён")





