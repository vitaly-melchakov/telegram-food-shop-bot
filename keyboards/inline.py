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

def main_inline_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🍔 Открыть каталог",
                    callback_data="back_to_categories"
                )
            ]
        ]
    )



def after_add_to_cart_kb(product_id: str, category: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛒 Перейти в корзину",
                    callback_data="cart:open"
                )
            ],
            [
                InlineKeyboardButton(
                    text="➕ Продолжить покупки",
                    callback_data="back_to_categories"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Открыть карточку товара",
                    callback_data=f"product:{product_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 К списку товаров",
                    callback_data=f"cat:{category}"
                )
            ],
        ]
    )



def remove_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Оформить заказ",
                    callback_data="cart:checkout"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🧹 Очистить корзину",
                    callback_data="cart:clear"
                )
            ],
            [
                InlineKeyboardButton(
                    text="➕ Продолжить покупки",
                    callback_data="back_to_categories"
                )
            ],
        ]
    )


def checkout_confirm_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить заказ",
                    callback_data="order:confirm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Вернуться в корзину",
                    callback_data="cart:open"
                )
            ],
            [
                InlineKeyboardButton(
                    text="➕ Продолжить покупки",
                    callback_data="back_to_categories"
                )
            ],
        ]
    )

def order_success_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🍔 Вернуться в каталог",
                    callback_data="back_to_categories"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Главное меню",
                    callback_data="main:menu"
                )
            ],
        ]
    )



def cart_inline_kb(cart: dict | None = None):
    keyboard = []

    if not cart:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text="➕ Продолжить покупки",
                    callback_data="back_to_categories"
                )
            ]
        )

        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    for product_id in cart:
        product = get_product_by_id(product_id)

        if product is None:
            continue

        name = product[1]

    keyboard.append(
        [
            InlineKeyboardButton(
                text="✅ Оформить заказ",
                callback_data="cart:checkout"
            )
        ]
    )

    keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"➖ {name}",
                    callback_data=f"cart:remove:{product_id}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="🧹 Очистить корзину",
                callback_data="cart:clear"
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="➕ Продолжить покупки",
                callback_data="back_to_categories"
            )
        ]
    )
    keyboard.append(
    [
        InlineKeyboardButton(
            text="🏠 Главное меню",
            callback_data="main:menu"
        )
    ]
)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)







def opisanie_kb(category):
    builder = InlineKeyboardBuilder()

    products = get_products_by_category(category)

    for product in products:
        builder.button(
            text=product[1],
            callback_data=f"product:{product[0]}"
        )

    builder.button(
        text="⬅️ Назад к категориям",
        callback_data="back_to_categories"
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