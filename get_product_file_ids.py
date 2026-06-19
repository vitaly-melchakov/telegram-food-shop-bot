import asyncio

from aiogram import Bot
from aiogram.types import FSInputFile

from config import BOT_TOKEN, ADMIN_ID


PRODUCT_IMAGES = {
    "p1": "AgACAgIAAxkDAAIRSGoxKgUXUiY8CapExe5BpSpYSGujAAJlHWsbCM-ISR_MSAtpWZybAQADAgADdwADPAQ",
    "p2": "AgACAgIAAxkDAAIRSWoxKgY3psbT4P7IhI2XFK1vXawQAAJmHWsbCM-ISWUE1-1A1B4TAQADAgADdwADPAQ",
    "p3": "AgACAgIAAxkDAAIRSmoxKgjq16FNHbNuVYjR-ahjug7jAAJnHWsbCM-ISXd8yolA3eSMAQADAgADdwADPAQ",
    "p4": "AgACAgIAAxkDAAIRS2oxKgmv1Ctf5Nk-Sk626TAwJJOTAAJoHWsbCM-ISRoWIU_n2SMoAQADAgADdwADPAQ",
    "p5": "AgACAgIAAxkDAAIRTGoxKgsVgN9MJsWnGe54xxPiQUYcAAJpHWsbCM-ISV0jBbMB3cpPAQADAgADdwADPAQ",
    "p6": "AgACAgIAAxkDAAIRTWoxKg3j-Gg1V-Ty9U9EQnfgpDyWAAJqHWsbCM-ISR32ROVwKB9_AQADAgADdwADPAQ",
    "p7": "AgACAgIAAxkDAAIRVGoxK3U70bQiUDP7Szx-bw4Z-XOqAAJ0HWsbCM-IScNEmR7PMKQ6AQADAgADdwADPAQ",
    "p8": "AgACAgIAAxkDAAIRVWoxK3ZXLku_ttrx6UWZla-SbCUtAAJ1HWsbCM-ISYhZXBncOLOnAQADAgADdwADPAQ",
    "p9": "AgACAgIAAxkDAAIRVmoxK3hmXMdadiAWdI3kya8SAQlPAAJ2HWsbCM-ISQzZsDb-gY73AQADAgADdwADPAQ",
}


async def main():
    bot = Bot(token=BOT_TOKEN)

    print("\nPRODUCT_FILE_IDS = {")

    for product_id, image_path in PRODUCT_IMAGES.items():
        message = await bot.send_photo(
            chat_id=ADMIN_ID,
            photo=FSInputFile(image_path),
            caption=f"file_id для товара {product_id}"
        )

        file_id = message.photo[-1].file_id

        print(f'    "{product_id}": "{file_id}",')

    print("}")

    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())