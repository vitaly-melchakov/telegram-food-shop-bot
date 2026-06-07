from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F
from aiogram.types import ReplyKeyboardRemove


from keyboards.reply import after_cart, confirm_order
from keyboards.inline import admin_order_kb

from states.shop import Shop


from datetime import datetime

from config import ADMIN_ID

from database import get_product_by_id, save_order



router = Router()
time = datetime.now()
formatted_date = time.strftime("%d-%m-%y %H:%M")

order_number = 0



@router.message(F.text == "Оплатить")
async def handler_payment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cart = data.get("cart", {})

    if not cart:
        await message.answer("Корзина пуста")
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

    order_text = (
        "Ваш заказ:\n\n"
        f"{order_items_text}\n"
        f"Итого: {total} дин"
        "\n\nПодтвердить заказ?"
    )
    await state.update_data(
        order_text=order_text,
        order_items_text=order_items_text,
        total=total
    )
    await state.set_state(Shop.confirming)

    await message.answer(order_text, reply_markup=confirm_order)
    

@router.message(Shop.confirming, F.text == "Подтвердить заказ")
async def handler_confirm_order(message: types.Message, state: FSMContext):
    data = await state.get_data()

    cart = data.get("cart", {})
    order_items_text = data.get("order_items_text", "Заказ без деталей")
    total = data.get("total", 0)

    if not cart:
        await message.answer("Корзина пустая.")
        return

    user = message.from_user

    order_id = save_order(
        user_id=user.id,
        username=user.username,
        full_name=user.full_name,
        cart=cart
    )

    admin_text = (
    f"🆕 Новый заказ №{order_id}!\n\n"
    f"Клиент: {user.full_name}\n"
    f"Username: @{user.username}\n"
    f"User ID: {user.id}\n\n"
    f"Заказ:\n"
    f"{order_items_text}\n"
    f"Итого: {total} дин\n\n"
    
    )
    await message.bot.send_message(ADMIN_ID, admin_text,
    reply_markup=admin_order_kb(order_id)
)

    await message.answer(
        f"✅ Заказ №{order_id} подтверждён. Мы скоро свяжемся с вами.",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.update_data(cart={})
    await state.clear()



@router.message(Shop.confirming, F.text == "Отмена")
async def cancel(message:types.Message, state:FSMContext ):
   await state.set_state(Shop.cart)
   await message.answer ("Отмена подтверждения", reply_markup=after_cart )

