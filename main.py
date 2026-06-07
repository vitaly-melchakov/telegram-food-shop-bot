import asyncio 
from aiogram import Bot, Dispatcher




from config import BOT_TOKEN

from handlers.start import router as start_router
from handlers.catalog import router as catalog_router
from handlers.cart import router as cart_router
from handlers.order import router as order_router
from handlers.admin import router as admin_router
from handlers.echo import router as echo_router
from database import (
    create_orders_table,
    orders_items_table,
    add_status_column_to_orders
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(admin_router)
dp.include_router(start_router)
dp.include_router(catalog_router)
dp.include_router(cart_router)
dp.include_router(order_router)
dp.include_router(echo_router)


async def main():
    create_orders_table()
    orders_items_table()   
    add_status_column_to_orders() # таблицы должны создаваться перед запуском
    await dp.start_polling(bot)
  

if __name__== "__main__":
    asyncio.run(main())