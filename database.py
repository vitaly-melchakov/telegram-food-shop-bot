import sqlite3
from datetime import datetime

def add_product(product_id, name, price, category, photo=None): 
 db = sqlite3.connect('shop.db') 

 cursor = db.cursor()   

 cursor.execute("""CREATE TABLE IF NOT EXISTS products (
                   id TEXT PRIMARY KEY,
                   name TEXT NOT NULL,
                   price INTEGER NOT NULL,
                   category TEXT NOT NULL,
                   photo TEXT
                   )   
               
               
               
               
                  """)   

 cursor.execute("""
    INSERT OR IGNORE INTO products (id, name, price, category, photo)
    VALUES (?, ?, ?, ?, ?)
""", (product_id, name, price, category, photo))


 db.commit() 

 db.close() 


def get_products_by_category(category):
    db = sqlite3.connect("shop.db")
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, name, price, category, photo
        FROM products
        WHERE category = ?
    """, (category,))  

    products = cursor.fetchall() 

    db.close()

    return products


def get_product_by_id(product_id):
    db = sqlite3.connect("shop.db")
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, name, price, category, photo
        FROM products
        WHERE id = ?
    """, (product_id,))

    product = cursor.fetchone() 

    db.close()

    return product


def create_orders_table():   
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER,
            username TEXT,
            full_name TEXT,
            total_price INTEGER,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()



def orders_items_table():
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            product_name TEXT,
            quantity INTEGER,
            price INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders(id) 
        )
    """)

    conn.commit()
    conn.close()
    

def save_order(user_id, username, full_name, cart):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    total_price = 0
    order_items = []

    for product_id, quantity in cart.items():
        product = get_product_by_id(product_id)

        if product is None:
            continue

        product_name = product[1]
        price = product[2] 

        total_price += price * quantity

        order_items.append({
            "product_id": product_id,
            "product_name": product_name,
            "quantity": quantity,
            "price": price
        })

    created_at =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO orders (user_id, username, full_name, total_price, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, username, full_name, total_price, created_at))

    order_id = cursor.lastrowid 

    for item in order_items:
        cursor.execute("""
            INSERT INTO order_items (order_id, product_id, product_name, quantity, price)
            VALUES (?, ?, ?, ?, ?)
        """, (
            order_id,
            item["product_id"],
            item["product_name"],
            item["quantity"],
            item["price"]
        ))

    conn.commit()
    conn.close()

    return order_id
   

def get_orders(limit=10):   
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            id,
            user_id,
            username,
            full_name,
            total_price,
            created_at,
            status
        FROM orders
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    orders = cursor.fetchall()

    conn.close()

    return orders



def get_orders_by_status(status, limit=10):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            id,
            user_id,
            username,
            full_name,
            total_price,
            created_at,
            status
        FROM orders
        WHERE status = ?
        ORDER BY id DESC
        LIMIT ?
    """, (status, limit))

    orders = cursor.fetchall()

    conn.close()

    return orders



def get_order_items(order_id):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT product_name, quantity, price
        FROM order_items
        WHERE order_id = ?
    """, (order_id,))

    items = cursor.fetchall()

    conn.close()

    return items

def add_status_column_to_orders():
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            ALTER TABLE orders     
            ADD COLUMN status TEXT DEFAULT 'new'
        """)
        conn.commit()
        print("Колонка status добавлена в orders")
    except sqlite3.OperationalError:
        print("Колонка status уже существует")

    conn.close()
    


def update_order_status(order_id, status): 
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE orders
        SET status = ?
        WHERE id = ?
    """, (status, order_id))

    conn.commit()
    conn.close()



products = [
    ("p1", "🍔 Classic", 690, "burgers", "images/classic.jpg"),
    ("p2", "🍔 Double", 750, "burgers", "images/double.png"),
    ("p3", "🍔 BBQ Jalapeño", 790, "burgers", "images/jalapeno.png"),
    ("p4", "🍟 Fries (150g)", 220, "sides", "images/fries.png"),
    ("p5", "🍗 Nuggets (9 pcs)", 250, "sides", "images/nuggets.png"),
    ("p6", "🥫 Sauce", 50, "sides", "images/sauce.png"),
    ("p7", "🥤 Coca-Cola 0.33", 120, "drinks", "images/cola.png"),
    ("p8", "🧃 Juice 0.33", 90, "drinks", "images/juice.png"),
    ("p9", "💧 Water 0.5", 70, "drinks", "images/water.png"),
]

for product in products:
    add_product(*product)

print(get_products_by_category("burgers"))



