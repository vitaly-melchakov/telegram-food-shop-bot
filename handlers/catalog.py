from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F

from keyboards.inline import inkb, add_kb, opisanie_kb, after_add_to_cart_kb, products_list_kb, start_kb

from states.shop import Shop

from aiogram.types import InputMediaPhoto, CallbackQuery
from database import get_product_by_id, get_products_by_category
from config import ADMIN_ID

from media import CATALOG_PHOTO_ID


from aiogram.exceptions import TelegramBadRequest




router = Router()

def get_catalog_banner_file():
    return CATALOG_PHOTO_ID

CATALOG_PHOTO = "images/catalog.png"


@router.message(F.text == "Каталог") 
async def handler_catalog(message:types.Message, state:FSMContext ):
    await state.set_state(Shop.catalog)   
    await message.answer ("Выберите категорию", reply_markup=inkb)
    


@router.callback_query(F.data.startswith("cat:"))
async def show_products_handler(callback: CallbackQuery):
    category = callback.data.split(":")[1]

    products = get_products_by_category(category)

    text = "Выберите товар:"

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=CATALOG_PHOTO_ID,
            caption=text
        ),
        reply_markup=products_list_kb(products)
    )

    await callback.answer()





@router.callback_query(F.data == "back_to_categories")
async def back_to_categories_handler(callback: CallbackQuery):
    text = (
        "🍔 Каталог\n\n"
        "Выберите категорию:"
    )

    media = InputMediaPhoto(
        media=CATALOG_PHOTO_ID,
        caption=text
    )

    try:
        await callback.message.edit_media(
            media=media,
            reply_markup=inkb
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            await callback.answer()
            return

        raise

    await callback.answer()


@router.callback_query(F.data.startswith("back_cat:"))
async def back_to_products(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Shop.catalog)

    category = callback.data.split(":", 1)[1]

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=CATALOG_PHOTO_ID,
            caption="🛒 Выберите товар:"
        ),
        reply_markup=opisanie_kb(category)
    )

    await callback.answer()
    


@router.callback_query(F.data.startswith("add:"))
async def callback_add(callback: types.CallbackQuery, state: FSMContext):
    product_id = callback.data.split(":", 1)[1]

    product = get_product_by_id(product_id)

    if product is None:
        await callback.answer("Товар не найден")
        return

    name = product[1]
    price = product[2]
    category = product[3]

    data = await state.get_data()
    cart = data.get("cart", {})

    cart[product_id] = cart.get(product_id, 0) + 1

    await state.update_data(cart=cart)

    text = (
    f"✅ Товар добавлен в корзину!\n\n"
    f"🍔 {name}\n"
    f"💰 Цена: {price} дин.\n\n"
    f"Можете оформить заказ или добавить ещё."
    )

    await callback.message.edit_caption(
        caption=text,
        reply_markup=after_add_to_cart_kb(product_id, category)
    )

    await callback.answer(f"✅ {name} добавлен в корзину")



@router.callback_query(F.data.startswith("product:"))
async def show_product_card(callback: CallbackQuery):
    parts = callback.data.split(":")

    if len(parts) < 2:
        await callback.answer("Ошибка кнопки товара", show_alert=True)
        return

    product_id = parts[1]

    product = get_product_by_id(product_id)

    if product is None:
        print("Товар не найден")
        print("callback.data =", callback.data)
        print("product_id =", product_id)

        await callback.answer("Товар не найден", show_alert=True)
        return

    name = product[1]
    price = product[2]
    category = product[3]
    photo = product[4]

    text = (
        f"🍔 {name}\n\n"
        f"💰 Цена: {price} дин."
    )

    media = InputMediaPhoto(
        media=photo,
        caption=text
    )

    await callback.message.edit_media(
        media=media,
        reply_markup=add_kb(product_id, category)
    )

    await callback.answer()


@router.message(F.text == "Продолжить покупки")
async def handler_continue_shopping(message:types.Message, state:FSMContext ):
    await state.set_state(Shop.catalog)  
    await message.answer ( "Выберите товар:", reply_markup=inkb)


@router.callback_query(F.data == "open_catalog")
async def open_catalog_handler(callback: CallbackQuery):
    text = (
        "🍔 Каталог\n\n"
        "Выберите категорию:"
    )

    media = InputMediaPhoto(
        media=CATALOG_PHOTO_ID,
        caption=text
    )

    if callback.message.photo:
        try:
            await callback.message.edit_media(
                media=media,
                reply_markup=inkb
            )
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                await callback.answer()
                return

            raise
    else:
        await callback.message.answer_photo(
            photo=CATALOG_PHOTO_ID,
            caption=text,
            reply_markup=inkb
        )

        try:
            await callback.message.delete()
        except TelegramBadRequest:
            pass

    await callback.answer()


@router.callback_query(F.data == "main_menu")
async def main_menu_handler(callback: CallbackQuery):
    is_admin = callback.from_user.id == ADMIN_ID

    text = (
        "🍔 Добро пожаловать!\n\n"
        "Выберите действие:"
    )

    media = InputMediaPhoto(
        media=CATALOG_PHOTO_ID,
        caption=text
    )

    await callback.message.edit_media(
        media=media,
        reply_markup=start_kb(is_admin=is_admin)
    )

    await callback.answer()