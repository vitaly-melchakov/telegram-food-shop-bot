from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F

from keyboards.inline import cart_inline_kb, checkout_confirm_kb

from database import get_product_by_id

router = Router()

from aiogram.types import InputMediaPhoto

from media import CART_PHOTO_ID


def get_cart_image():
    return CART_PHOTO_ID

def build_cart_text(cart: dict) -> str:
    if not cart:
        return (
            "🛒 Корзина пуста.\n\n"
            "Можете вернуться в каталог и выбрать товары."
        )

    text = "🛒 Ваш заказ:\n\n"
    total = 0

    for product_id, quantity in cart.items():
        product = get_product_by_id(product_id)

        if product is None:
            continue

        name = product[1]
        price = product[2]

        subtotal = price * quantity
        total += subtotal

        text += f"🍔 {name} x{quantity} — {subtotal} дин.\n"

    text += f"\n💰 Итого: {total} дин."

    return text


@router.callback_query(F.data == "cart:open")
async def callback_open_cart(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    cart = data.get("cart", {})

    text = build_cart_text(cart)

    if callback.message.photo:
        media = InputMediaPhoto(
            media=get_cart_image(),
            caption=text
        )

        await callback.message.edit_media(
            media=media,
            reply_markup=cart_inline_kb(cart)
        )
    else:
        await callback.message.delete()

        await callback.message.answer_photo(
            photo=get_cart_image(),
            caption=text,
            reply_markup=cart_inline_kb(cart)
        )

@router.callback_query(F.data == "cart:clear")
async def callback_clear_cart(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(cart={})

    text = (
        "🧹 Корзина очищена.\n\n"
        "Можете вернуться в каталог и выбрать товары заново."
    )

    await callback.message.edit_caption(
        caption=text,
        reply_markup=cart_inline_kb({})
    )

    await callback.answer("Корзина очищена")


@router.callback_query(F.data == "cart:checkout")
async def callback_checkout(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cart = data.get("cart", {})

    if not cart:
        await callback.message.edit_caption(
            caption=(
                "🛒 Корзина пуста.\n\n"
                "Сначала добавьте товары в корзину."
            ),
            reply_markup=cart_inline_kb()
        )
        await callback.answer("Корзина пуста")
        return

    text = build_cart_text(cart)

    text += (
        "\n\nПодтвердите оформление ниже 👇"
    )

    await callback.message.edit_caption(
        caption=text,
        reply_markup=checkout_confirm_kb()
    )

    await callback.answer()


@router.callback_query(F.data.startswith("cart:remove:"))
async def callback_remove_from_cart(callback: types.CallbackQuery, state: FSMContext):
    product_id = callback.data.split(":", 2)[2]

    data = await state.get_data()
    cart = data.get("cart", {})

    if product_id not in cart:
        await callback.answer("Товара уже нет в корзине")
        return

    cart[product_id] -= 1

    if cart[product_id] <= 0:
        del cart[product_id]

    await state.update_data(cart=cart)

    text = build_cart_text(cart)

    await callback.message.edit_caption(
        caption=text,
        reply_markup=cart_inline_kb(cart)
    )

    await callback.answer("Товар удалён")




   
   
   




    
    
