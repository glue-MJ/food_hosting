from backend_web import sql, pd

def query_sql(PATH_SQL: str, fetch: bool):
    with sql.connect(PATH_SQL) as conn:
        cur = conn.execute(PATH_SQL)
        cur.execute(PATH_SQL)
        if fetch:
            return cur.fetchall()
        conn.commit()
    return 0

def initialize_products(PATH_SQL: str):
    with sql.connect(PATH_SQL) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS PRODUCTS(
            ID_PRODUCT INTEGER PRIMARY KEY,
            NAME TEXT,
            DESCRIPTION TEXT,
            ID_STALL
        );
        """)
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