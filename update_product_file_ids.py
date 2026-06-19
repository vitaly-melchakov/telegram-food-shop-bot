import sqlite3


PRODUCT_FILE_IDS = {
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


db = sqlite3.connect("shop.db")
cursor = db.cursor()

for product_id, file_id in PRODUCT_FILE_IDS.items():
    cursor.execute(
        """
        UPDATE products
        SET photo = ?
        WHERE id = ?
        """,
        (file_id, product_id)
    )

db.commit()

cursor.execute("""
    SELECT id, name, photo
    FROM products
""")

products = cursor.fetchall()

for product in products:
    print(product)

db.close()

print("Готово: file_id товаров обновлены.")