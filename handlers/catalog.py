from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F

from keyboards.inline import inkb, add_kb, opisanie_kb
from keyboards.reply import after_cart

from states.shop import Shop

from aiogram.types import FSInputFile
from database import get_product_by_id




router = Router()

@router.message(F.text == "Каталог") 
async def handler_catalog(message:types.Message, state:FSMContext ):
    await state.set_state(Shop.catalog)   #пользователь в каталоге
    await message.answer ("Выбери категорию", reply_markup=inkb)
    



@router.callback_query(Shop.catalog, F.data.startswith("cat:"))  #пользователь выбрал категорию
async def callback_cat(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data.split(":", 1)[1]  

    await callback.message.answer ("Выбери товар 🛒", reply_markup=opisanie_kb(category))
    await callback.answer()  #чтобы кнопка не залипала просто


@router.callback_query(Shop.catalog, F.data.startswith("back_cat:")) # пользовать вернулся назад к категориям
async def callback_back_cat(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data.split(":", 1)[1]  
    await callback.message.answer ("Выбери товар 🛒", reply_markup=opisanie_kb(category))
    await callback.answer()  #чтобы кнопка не залипала просто

    


@router.callback_query(F.data.startswith("add:"))
async def callback_add(callback: types.CallbackQuery, state: FSMContext):
    product_id = callback.data.split(":", 1)[1]

    product = get_product_by_id(product_id)

    if product is None:
        await callback.answer("Товар не найден")
        return

    name = product[1]

    data = await state.get_data()
    cart = data.get("cart", {})

    cart[product_id] = cart.get(product_id, 0) + 1

    await state.update_data(cart=cart)

    await callback.answer(f"{name} добавлен в корзину")
    await callback.message.answer(
    "Товар добавлен в корзину 🛒",
    reply_markup=after_cart
)



@router.callback_query(Shop.catalog, F.data.startswith("product:"))
async def callback_product(callback: types.CallbackQuery, state: FSMContext):
    product_id = callback.data.split(":", 1)[1]

    product = get_product_by_id(product_id)

    if product is None:
        await callback.answer("Товар не найден")
        return

    product_id = product[0]
    name = product[1]
    price = product[2]
    category = product[3]
    photo = product[4]

    text = f"{name}\n\nЦена: {price} дин"

    await callback.message.answer_photo(
        photo=FSInputFile(photo),
        caption=text,
        reply_markup=add_kb(product_id, category)
    )

    await callback.answer()


@router.message(F.text == "Продолжить покупки")
async def handler_catalog(message:types.Message, state:FSMContext ):
    await state.set_state(Shop.catalog)   #пользователь в каталоге
    await message.answer ( "Выбери товар:", reply_markup=inkb)