from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F

from keyboards.inline import cart_inline_kb, checkout_confirm_kb, remove_kb, empty_cart_inline_kb

from database import get_product_by_id
router = Router()

from aiogram.types import InputMediaPhoto, CallbackQuery

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


@router.callback_query(F.data == "cart")
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

    await callback.message.edit_caption(
        caption=(
            "🛒 Ваша корзина пуста.\n\n"
            "Добавьте товары из каталога."
        ),
        reply_markup=empty_cart_inline_kb()
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
            reply_markup=empty_cart_inline_kb()
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


@router.callback_query(F.data.startswith("remove:"))
async def remove_from_cart(callback: CallbackQuery, state: FSMContext):
    product_id = callback.data.split(":", 1)[1]

    data = await state.get_data()
    cart = data.get("cart", {})

    if product_id not in cart:
        await callback.answer("Этого товара уже нет в корзине", show_alert=True)
        return

    if cart[product_id] > 1:
        cart[product_id] -= 1
    else:
        del cart[product_id]

    await state.update_data(cart=cart)

    if not cart:
        text = (
            "🛒 Ваша корзина пуста.\n\n"
            "Добавьте товары из каталога."
        )

        await callback.message.edit_caption(
            caption=text,
            reply_markup=remove_kb()
        )

        await callback.answer("Товар удалён")
        return

    text = "🛒 Ваш заказ:\n\n"
    total = 0

    for cart_product_id, quantity in cart.items():
        product = get_product_by_id(cart_product_id)

        if product is None:
            continue

        name = product[1]
        price = product[2]

        item_total = price * quantity
        total += item_total

        text += f"🍔 {name} x{quantity} — {item_total} дин.\n"

    text += f"\n💰 Итого: {total} дин."

    await callback.message.edit_caption(
        caption=text,
        reply_markup=cart_inline_kb(cart)
    )

    await callback.answer("Товар удалён")




   
   
   




    
    
