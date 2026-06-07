from aiogram import types, Router

router =Router()

@router.message()
async def echo(message:types.Message ):
    await message.answer ("Вот список доступных команд :\n"
                          "/start - старт ботямбы\n"
                          "/menu - возврат в меню\n"
                          "/admin_help - панель админа")
