from backend_web import sql, os, UserMixin, dataclass, FlaskForm, pd
from backend_web import functions as func

path_sql = os.path.join(os.getcwd(), "storage.db")

class InitializeDataBase(object):
    def __init__(self):
        self.path = os.path.join(os.getcwd(), "storage.db")

    def activate(self):
        PATH_SQL = self.path
        func.initialize_customers(PATH_SQL)
        func.initialize_products(PATH_SQL)
        func.initialize_stall(PATH_SQL)
        func.initalize_order(PATH_SQL)
        func.initialize_track(PATH_SQL)

    def __repr__(self):
        return super().__repr__()

@dataclass
class Customers(UserMixin):
    Cus_Id: int
    Name: str
    Password: str
    Email: str
    Phone: str
    Credit_Card: str
        
    @classmethod
    def retrieve_person(cls: object, id_: int):
        data = func.query_sql(path_sql, f"SELECT * FROM CUSTOMERS WHERE ID = {id_};", True)
        return cls(*data)

    def register(self):
        self.Cus_Id = "NULL"
        func.query_sql(path_sql, f"INSERT INTO CUSTOMERS (ID_CUSTOMERS, NAME, PASSWORD, EMAIL, PHONE, CREDIT_CARD) VALUES {self.Cus_ID, self.Name, self.Password, self.Email, self.Phone, self.Credit_Card}", False)
        return self

    def is_authenticated(self):
        return super().is_authenticated

@dataclass
class Stall(object):
    Stall_ID: int
    Name: str
    Password: str
    Account: str
    Phone: str

    @classmethod
    def retrieve_info(cls: object, Account: str, Password: str):
        data = func.query_sql(path_sql, f"SELECT * FROM STALL WHERE ACCOUNT = {Account} AND PASSWORD = {Password};", True)
        return cls(*data)

    def register(self):
        self.Stall_ID = "NULL"
        func.query_sql(path_sql, f"INSERT INTO STALL (ID_STALL, NAME, PASSWORD, ACCOUNT, PHONE) VALUES {func.r_attr(self)}", False)
        return self

@dataclass
class Products(object):
    ID_PRODUCT: int
    NAME: str
    DESCRIPTION: str
    ID_STALL: int
    PRICE: float

    @staticmethod
    def query_food(search: str):  # SEARCHES FOR FOOD
        txt = f"SELECT * FROM PRODUCTS WHERE NAME LIKE '%{search}%'"
        df_result = func.sql_tables(path_sql, txt)
        if df_result.values.size != 0:  # IF TABLE IS NOT EMPTY
            return df_result
        return func.sql_tables(path_sql, f'SELECT * FROM PRODUCTS')

    def add_food(self):
        self.ID_PRODUCT = "NULL"
        func.query_sql(path_sql, f"INSERT INTO PRODUCTS {func.r_col(self)} VALUES {func.r_attr(self)}", False)
        return self
    
    @staticmethod
    def update_food(ID_Product: int, **kwargs):
        col = Products.__annotations__
        new_dict = (f'{i} = {j}' for i, j in kwargs.items() if (i in col and type(j) == col[i]))
        update_str = f'UPDATE PRODUCTS SET {new_dict} WHERE ID_PRODUCT = {ID_Product};'
        func.query_sql(path_sql, update_str, False)

    @staticmethod
    def delete_food(ID_Product: int):
        func.query_sql(path_sql, f'DELETE FROM PRODUCTS WHERE ID_Product = {ID_Product}')
        return 0

@dataclass
class Orders(object):
    ID_ORDER: int
    ID_PRODUCT: int
    STATUS: str
    SPECIAL_REQUESTS: str
    PHONE: str
    ID_CUSTOMER: int

    def new_order(self):
        self.ID_ORDER = "NULL"
        txt = f'INSERT INTO ORDERS {func.r_col(self)} VALUES {func.r_attr(self)}'
        func.query_sql(path_sql, txt, False)
        return self

    @classmethod
    def retrieve_order(cls: object, ID_ORDER: int):
        txt = f'SELECT * FROM ORDERS WHERE ID_ORDER = {ID_ORDER}'
        data = func.query_sql(path_sql, txt, True)
        return cls(*data)


@dataclass
class Track(object):
    ID_BOX: int
    ID_ORDER: int
    ID_STALL: int
    STATUS: str

    @staticmethod
    def ALLOCATE(ID_ORDER: int, ID_STALL: int):
        txt = f'SELECT ID_BOX FROM TRACK WHERE STATUS = "UNOCCUPIED" LIMIT 1'
        data = func.query_sql(path_sql, txt, True)
        if data == None:
            return -1
        txt_2 = f'UPDATE TRACK SET ID_ORDER = {ID_ORDER}, ID_STALL = {ID_STALL}, STATUS = "OCCUPIED" WHERE ID_BOX = {data[0]}'
        func.query_sql(path_sql, txt_2, False)
        return 0

    @staticmethod
    def COMPLETE(ID_BOX: int):
        txt = f'UPDATE STATUS = "UNOCCUPIED" WHERE ID_BOX = {ID_BOX}'
        func.query_sql(path_sql, txt, False)
        return 0