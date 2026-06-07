# Telegram Food Shop Bot

Telegram-бот для оформления заказов еды с корзиной, SQLite-базой данных и админ-панелью.

## Возможности

- Просмотр категорий товаров
- Просмотр карточек товаров
- Добавление товаров в корзину
- Удаление товаров из корзины
- Очистка корзины
- Оформление заказа
- Сохранение заказов в SQLite
- Уведомление администратора о новом заказе
- Админские команды для просмотра заказов
- Фильтрация заказов по статусам
- Изменение статуса заказа
- Inline-кнопки администратора для управления заказами

## Технологии

- Python
- aiogram
- SQLite
- python-dotenv

## Структура проекта

```text
.
├── main.py
├── config.py
├── database.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── handlers/
│   ├── start.py
│   ├── catalog.py
│   ├── cart.py
│   ├── order.py
│   ├── admin.py
│   └── echo.py
├── keyboards/
│   ├── reply.py
│   ├── inline.py
│   └── admin_kb.py
├── states/
│   └── shop.py
├── images/
│   ├── classic.jpg
│   ├── double.png
│   ├── Jalapeno.png
│   ├── fries.png
│   ├── nuggets.png
│   ├── sauce.png
│   ├── coca-cola.png
│   ├── juice.png
│   └── water.png
└── screenshots/
    ├── start.jpg
    ├── categories.jpg
    ├── product.jpg
    ├── cart.jpg
    ├── order_confirm.jpg
    ├── admin_order.jpg
    └── admin_status.jpg
```

## Установка и запуск

1. Клонировать репозиторий:

```bash
git clone https://github.com/vitaly-melchakov/telegram-food-shop-bot.git
```

2. Перейти в папку проекта:

```bash
cd telegram-food-shop-bot
```

3. Создать виртуальное окружение:

```bash
python -m venv .venv
```

4. Активировать виртуальное окружение.

Для Windows:

```bash
.venv\Scripts\activate
```

5. Установить зависимости:

```bash
python -m pip install -r requirements.txt
```

6. Создать файл `.env` в корне проекта:

```env
BOT_TOKEN=your_bot_token
ADMIN_ID=your_telegram_id
```

7. Запустить бота:

```bash
python main.py
```

## Переменные окружения

Проект использует файл `.env` для хранения секретных данных.
Пример файла `.env`:

```env
BOT_TOKEN=your_bot_token
ADMIN_ID=your_telegram_id
```

Описание переменных:

- `BOT_TOKEN` — токен Telegram-бота, полученный через BotFather
- `ADMIN_ID` — Telegram ID администратора, который получает заказы и управляет их статусами

Файл `.env` не загружается на GitHub, потому что содержит секретные данные.

Для примера используется файл `.env.example`.

## Админ-панель

Администратор получает уведомление о новом заказе и может управлять заказами через команды и inline-кнопки.

Доступные команды администратора:

```text
/orders
/orders_new
/orders_done
/orders_cancelled
/order_done ID
/order_new ID
/order_cancel ID
/admin_help
```

Статусы заказов:

```text
new
done
cancelled
```

## База данных

Проект использует SQLite.

В базе данных используются таблицы:

- `products` — товары
- `orders` — заказы
- `order_items` — товары внутри заказов

Локальный файл базы данных `shop.db` не загружается на GitHub.

## Автор

Проект создан как учебный Telegram-бот на Python/aiogram для портфолио.

Автор: Vitaly Melchakov

## Контакты

- GitHub: https://github.com/vitaly-melchakov
- Telegram: @pomposso