import sqlite3 as sql
from backend_web import path_sql
from backend_web import functions as func
from backend_web import models as mdls
import json

with open("products.json") as file:
    dic = json.load(file)
    print(dic.get(1))

# with sql.connect(path_sql) as conn:
#     cur = conn.cursor()
#     a = None
#     # txt = f"INSERT INTO 'CUSTOMERS' (ID_CUSTOMERS, NAME, PASSWORD, EMAIL, PHONE, CREDIT_CARD) VALUES (NULL, 'glueMJ', 'abc', 'quahmingjun@gmail.com', '88266598', '1234567812345678')"
#     # cur.execute(f"SELECT ID_CUSTOMERS FROM CUSTOMERS WHERE NAME = 'glueMJ'")
    # txt = f'DELETE FROM CUSTOMERS WHERE NAME = "glueMJ";'
#     txt = f''
#     cur.execute(txt)
#     print(cur.fetchone())
    # conn.commit()

# func.initialize_products(path_sql)

# mdls.Stall(0, "THE FOODIE", "PI_STORE", "PI", 88266598).register()

# mdls.Products(0, "Chicken Rice", "God Tier Food", 1, 2.50).add_food()
# mdls.Products(0, "Fish N Chips", "God Tier Food", 1, 5.00).add_food()
# mdls.Products(0, "McSpicy", "God Tier Food", 1, 5.00).add_food()
# mdls.Products(0, "Pancakes", "God Tier Food", 1, 1.80).add_food()
# mdls.Products(0, "Hashbrowns", "God Tier Food", 1, 1.50).add_food()

# with sql.connect(path_sql) as conn:
#     cur = conn.cursor()
#     ID_STALL = 1
#     txt = f'SELECT * FROM ORDERS INNER JOIN PRODUCTS USING (ID_PRODUCT) WHERE ID_STALL = {ID_STALL} AND STATUS = "CARTED";'
#     cur.execute(txt)
#     print(cur.fetchall())
#     print(next(zip(*cur.description)))