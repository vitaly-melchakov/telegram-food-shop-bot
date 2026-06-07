from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F

from keyboards.reply import after_cart
from keyboards.inline import inkb, remove_kb

from states.shop import Shop

from database import get_product_by_id

router = Router()

@router.message(F.text == "Корзина")
async def handler_cart(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cart = data.get("cart", {})

    if not cart:
        await message.answer("Корзина пуста")
        return

    text = "🛒 Ваша корзина:\n\n"
    total = 0

    for product_id, quantity in cart.items():  
        product = get_product_by_id(product_id)

        if product is None:
            continue

        name = product[1]
        price = product[2]

        subtotal = price * quantity
        total += subtotal

        text += f"{name} x{quantity} — {subtotal} дин\n"

    text += f"\nИтого: {total} дин"

    await message.answer(text, reply_markup=after_cart)

   
   
   
@router.callback_query(F.data.startswith("remove:"))
async def callback_remove(callback: types.CallbackQuery, state: FSMContext):
    product_id = callback.data.split(":", 1)[1]  

    data = await state.get_data()
    cart = data.get("cart", {})

    if product_id in cart:
     cart[product_id]-=1

    if cart[product_id] <= 0:
     del cart[product_id]

    if not cart:
     await callback.message.answer ("Корзина пуста", reply_markup=after_cart) 
     return 

    await state.update_data(cart=cart)

    lines = []
    total = 0
    for product_id, qty in cart.items():
     product_name = get_product_by_id(product_id)
     name = product_name.get("name")
     price = product_name.get("price")
     item_total = qty * price
     total = item_total + total
     lines.append(f"• {name} × {qty} = {price} дин")

    text = "🛒 Ваша корзина:\n" + "\n".join(lines) + f"\n Итого: {total}"
    

    await callback.answer ("Товар удален") 
    await callback.message.answer(text) 
    await callback.message.answer("Редактировать корзину :", reply_markup=remove_kb(cart))



    
    
@router.message(F.text == "Очистить корзину")
async def clear_cart(message:types.Message, state:FSMContext ):
    await state.update_data (cart = {})
    await state.set_state(Shop.catalog)
    await message.answer ("Корзина очищена.\n Выбери товар:", reply_markup=inkb)