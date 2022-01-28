from backend_web import sql, pd

def query_sql(PATH_SQL: str, Query: str, fetch: bool):
    with sql.connect(PATH_SQL) as conn:
        cur = conn.execute(PATH_SQL)
        cur.execute(Query)
        if fetch:
            return cur.fetchone()
        conn.commit()
    return 0

def sql_tables(PATH_SQL: str, Query: str):
    with sql.connect(PATH_SQL) as conn:
        cur = conn.cursor()
        cur.execute(Query)
        col = next(zip(*cur.description))
        df = pd.DataFrame.from_records(cur.fetchall(), columns=col)
        conn.commit()
        return df

def initialize_products(PATH_SQL: str):
    with sql.connect(PATH_SQL) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS PRODUCTS(
            ID_PRODUCT INTEGER PRIMARY KEY,
            NAME TEXT,
            DESCRIPTION TEXT,
            ID_STALL INTEGER
            PRICE REAL
        );
        """)
        conn.commit()
    return 0

def initialize_customers(PATH_SQL: str):
    with sql.connect(PATH_SQL) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS CUSTOMERS(
            ID_CUSTOMERS INTEGER PRIMARY KEY,
            NAME TEXT,
            PASSWORD TEXT,
            EMAIL TEXT,
            PHONE TEXT,
            CREDIT_CARD TEXT
        );
        """)
        conn.commit()
    return 0

def initialize_stall(PATH_SQL: str):
    with sql.connect(PATH_SQL) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS STALL(
            ID_STALL INTEGER PRIMARY KEY,
            NAME TEXT,
            PASSWORD TEXT,
            ACCOUNT TEXT,
            PHONE TEXT
        );
        """)
    return 0

def initalize_order(PATH_SQL: str):
    with sql.connect(PATH_SQL) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS ORDERS(
            ID_ORDER INTEGER PRIMARY KEY,
            ID_PRODUCT INTEGER,
            STATUS TEXT,
            SPECIAL_REQUESTS TEXT,
            PHONE_NO TEXT,
            ID_CUSTOMER INTEGER
        );
        """)
    return 0

def initialize_track(PATH_SQL: str):
    with sql.connect(PATH_SQL) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS TRACK(
            ID_BOX INTEGER PRIMARY KEY,
            ID_ORDER INTEGER NULL,
            ID_STALL INTEGER NULL,
            STATUS TEXT
        );
        """)
    return 0

def r_attr(self):  # RETURNS THE VALUES OF AN INSTANCE VARIABLES
    return (*vars(self).values(),)

def r_col(self):  # RETURNS THE PROPERTIES OF A CLASS OR INSTANCE
    if type(self) == type(type):  # CHECK IF ITS AN CLASS OR INSTANCE OF A CLASS
        tup = range(self.__init__.__code__.co_argcount - 1)
        self = self(*tup)
    return (*self.__dict__,)