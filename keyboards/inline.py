from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router


from database import get_products_by_category, get_product_by_id

router = Router()

inkb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🍔 Burgers", callback_data="cat:burgers")],
    [InlineKeyboardButton(text="🍟 Sides", callback_data="cat:sides")],
    [InlineKeyboardButton(text="🥤Drinks", callback_data="cat:drinks")]
]
)


def remove_kb(cart):
   builder = InlineKeyboardBuilder()

   for product_id in cart:
     product = get_product_by_id(product_id, f"Неизвестный товар ({product_id})")
     name = product["name"]
     builder.button(text=f"Удалить {name}", callback_data = (f"remove:{product_id}"))
   
   builder.adjust(1)
   return builder.as_markup()

def opisanie_kb(category):
    builder = InlineKeyboardBuilder()

    products = get_products_by_category(category)

    for product in products:
        product_id = product[0]
        name = product[1]

        builder.button(
            text=name,
            callback_data=f"product:{product_id}"
        )

    builder.adjust(1)
    return builder.as_markup()

def add_kb(product_id, category):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Добавить в корзину",
        callback_data=f"add:{product_id}"
    )

    builder.button(
        text="Назад к товарам",
        callback_data=f"back_cat:{category}"
    )

    builder.adjust(1)
    return builder.as_markup()

def admin_order_kb(order_id: int):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Выполнен",
                    callback_data=f"admin_done:{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Отменить",
                    callback_data=f"admin_cancel:{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Новый",
                    callback_data=f"admin_new:{order_id}"
                )
            ]
        ]
    )

    return keyboard