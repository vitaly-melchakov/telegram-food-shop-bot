from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router


from database import get_products_by_category, get_product_by_id

router = Router()

inkb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🍔 Burgers",
                callback_data="cat:burgers"
            )
        ],
        [
            InlineKeyboardButton(
                text="🍟 Sides",
                callback_data="cat:sides"
            )
        ],
        [
            InlineKeyboardButton(
                text="🥤 Drinks",
                callback_data="cat:drinks"
            )
        ],
        [
            InlineKeyboardButton(
                text="🏠 Главное меню",
                callback_data="main_menu"
            )
        ]
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


def start_kb(is_admin: bool = False):
    buttons = [
        [
            InlineKeyboardButton(
                text="🍔 Открыть каталог",
                callback_data="open_catalog"
            )
        ]
    ]

    if is_admin:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="👨‍💻 Админ-панель",
                    callback_data="admin_panel"
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def after_add_to_cart_kb(product_id, category):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅ Оформить заказ",
        callback_data="cart:checkout"
    )

    builder.button(
        text="🛒 Посмотреть корзину",
        callback_data="cart"
    )

    builder.button(
        text="➕ Добавить ещё",
        callback_data="back_to_categories"
    )

    builder.adjust(1)
    return builder.as_markup()


def products_list_kb(products):
    buttons = []

    for product in products:
        product_id = product[0]
        name = product[1]
        price = product[2]

        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{name} — {price} дин.",
                    callback_data=f"product:{product_id}"
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="🔙 К категориям",
                callback_data="back_to_categories"
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)

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
                    callback_data="cart"
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



def cart_inline_kb(cart: dict):
    buttons = []

    buttons.append(
        [
            InlineKeyboardButton(
                text="✅ Оформить заказ",
                callback_data="cart:checkout"
            )
        ]
    )

    for product_id, quantity in cart.items():
        product = get_product_by_id(product_id)

        if product is None:
            continue

        name = product[1]

        buttons.append(
        [
            InlineKeyboardButton(
                text=f"❌ Убрать {name} x{quantity}",
                 callback_data=f"remove:{product_id}"
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                text="🧹 Очистить корзину",
                callback_data="cart:clear"
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                text="➕ Продолжить покупки",
                callback_data="back_to_categories"
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                text="🏠 Главное меню",
                callback_data="main_menu"
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)







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
                    text="🆕 Отметить как новый",
                    callback_data=f"admin_new:{order_id}"
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
                    text="👨‍💻 Админ-панель",
                    callback_data="admin_panel"
                )
            ]
        ]
    )

    return keyboard

def empty_cart_inline_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Продолжить покупки",
                    callback_data="back_to_categories"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Главное меню",
                    callback_data="main_menu"
                )
            ]
        ]
    )