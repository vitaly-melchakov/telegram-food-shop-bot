from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F

from keyboards.inline import inkb, add_kb, opisanie_kb, after_add_to_cart_kb

from states.shop import Shop

from aiogram.types import InputMediaPhoto
from database import get_product_by_id


from media import CATALOG_PHOTO_ID




router = Router()

def get_catalog_banner_file():
    return CATALOG_PHOTO_ID

CATALOG_PHOTO = "images/catalog.png"


@router.message(F.text == "Каталог") 
async def handler_catalog(message:types.Message, state:FSMContext ):
    await state.set_state(Shop.catalog)   
    await message.answer ("Выберите категорию", reply_markup=inkb)
    


@router.callback_query(Shop.catalog, F.data.startswith("cat:"))
async def callback_cat(callback: types.CallbackQuery):
    category = callback.data.split(":", 1)[1]

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=CATALOG_PHOTO_ID,
            caption="🛒 Выберите товар:"
        ),
        reply_markup=opisanie_kb(category)
    )

    await callback.answer()






@router.callback_query(F.data == "back_to_categories")
async def callback_back_to_categories(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Shop.catalog)

    # Если текущее сообщение уже с фото — просто меняем media
    if callback.message.photo:
        media = InputMediaPhoto(
            media=get_catalog_banner_file(),
            caption="🍔 Выберите категорию:"
        )

        await callback.message.edit_media(
            media=media,
            reply_markup=inkb
        )

    # Если текущее сообщение обычное текстовое — отправляем фото заново
    else:
        await callback.message.answer_photo(
            photo=get_catalog_banner_file(),
            caption="🍔 Выберите категорию:",
            reply_markup=inkb
        )

        await callback.message.delete()


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
        f"Что делаем дальше?"
    )

    await callback.message.edit_caption(
        caption=text,
        reply_markup=after_add_to_cart_kb(product_id, category)
    )

    await callback.answer(f"✅ {name} добавлен в корзину")



@router.callback_query(Shop.catalog, F.data.startswith("product:"))
async def callback_product(callback: types.CallbackQuery):
    product_id = callback.data.split(":", 1)[1]

    product = get_product_by_id(product_id)

    if product is None:
        await callback.answer("Товар не найден")
        return

    product_id = product[0]
    name = product[1]
    price = product[2]
    category = product[3]
    product_photo = product[4]

    text = (
        f"🍔 {name}\n\n"
        f"💰 Цена: {price} дин\n\n"
        f"Добавьте товар в корзину или вернитесь назад."
    )

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=product_photo,
            caption=text
        ),
        reply_markup=add_kb(product_id, category)
    )

    await callback.answer()


@router.message(F.text == "Продолжить покупки")
async def handler_continue_shopping(message:types.Message, state:FSMContext ):
    await state.set_state(Shop.catalog)  
    await message.answer ( "Выберите товар:", reply_markup=inkb)