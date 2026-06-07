from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router 

router = Router()

main_menu =  ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Главное меню")],
],
resize_keyboard=True
)


keyboard  = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Каталог"), KeyboardButton(text="Корзина")],
],
resize_keyboard=True
)

after_cart = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Продолжить покупки"), KeyboardButton(text="Оплатить")],
    [KeyboardButton(text="Корзина"), KeyboardButton(text="Очистить корзину")]
],
resize_keyboard=True
)

confirm_order =  ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Подтвердить заказ"), KeyboardButton(text="Отмена")],
],
resize_keyboard=True
)