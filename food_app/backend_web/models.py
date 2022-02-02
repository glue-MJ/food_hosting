from backend_web import sql, os, UserMixin, dataclass, FlaskForm, pd
from backend_web import functions as func
from flask import Flask
from wtforms import StringField, EmailField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, DataRequired, Email, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
import json

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
        data = func.query_sql(path_sql, f"SELECT * FROM CUSTOMERS WHERE ID_CUSTOMERS = {id_};", True)
        return cls(*data)

    @classmethod
    def signin(cls: object, name: str, password: str):
        txt = f'SELECT * FROM CUSTOMERS WHERE NAME = "{name}" AND PASSWORD = "{password}";'
        data = func.query_sql(path_sql, txt, True)
        return cls(*data)

    def register(self):
        lst = [types(i) for i, types in zip(self.__dict__.values(), self.__annotations__.values())]
        self.Cus_Id = "NULL"
        txt = f"INSERT INTO CUSTOMERS (ID_CUSTOMERS, NAME, PASSWORD, EMAIL, PHONE, CREDIT_CARD) VALUES {func.NULL_FIRST(lst)}"
        print(txt)
        func.query_sql(path_sql, txt, False)
        return self

    def is_authenticated(self):
        return super().is_authenticated

    def get_id(self):
        return self.Cus_Id

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

    @staticmethod
    def retrieve_info2(ID: int, Account: str, Password: str):
        data = func.sql_tables(path_sql, f"SELECT * FROM STALL WHERE ACCOUNT = {Account} AND PASSWORD = {Password};", True)
        return data

    def register(self):
        VAL = func.NULL_FIRST(func.r_attr(self))
        func.query_sql(path_sql, f"INSERT INTO STALL (ID_STALL, NAME, PASSWORD, ACCOUNT, PHONE) VALUES {VAL}", False)
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
        VAL = func.NULL_FIRST(func.r_attr(self))
        func.query_sql(path_sql, f"INSERT INTO PRODUCTS {func.r_col(self)} VALUES {VAL}", False)
        ID_PRODUCT = func.query_sql(path_sql, f"SELECT ID_PRODUCT FROM PRODUCTS ORDER BY ID_PRODUCTS DESC LIMIT 1;", True)
        if ID_PRODUCT:
            with open("products.json") as file:
                dic = json.load(file)
                dic = {**dic, **{f'{ID_PRODUCT}':"Food_BackGround.jpg"}}
        return self
    
    @staticmethod
    def update_food(ID_PRODUCT: int, **kwargs):
        col = Products.__annotations__
        new_dict = (f'{i} = {j}' for i, j in kwargs.items() if (i in col and type(j) == col[i]))
        update_str = f'UPDATE PRODUCTS SET {new_dict} WHERE ID_PRODUCT = {ID_PRODUCT};'
        func.query_sql(path_sql, update_str, False)

    @staticmethod
    def delete_food(ID_Products: list):
        for ID_Product in ID_Products:
            func.query_sql(path_sql, f'DELETE FROM PRODUCTS WHERE ID_Product = {ID_Product};', False)
        return 0

@dataclass
class Orders(object):
    ID_ORDER: int
    ID_PRODUCT: int
    STATUS: str    # CARTED, PENDING, PREPARING, U_READY, P_READY ,COLLECTED
    SPECIAL_REQUESTS: str
    PHONE_NO: str
    ID_CUSTOMER: int

    def new_order(self):
        VAL = func.NULL_FIRST(func.r_attr(self))
        txt = f'INSERT INTO ORDERS {func.r_col(self)} VALUES {VAL}'
        func.query_sql(path_sql, txt, False)
        return self

    @classmethod
    def retrieve_order(cls: object, ID_ORDER: int):
        txt = f'SELECT * FROM ORDERS WHERE ID_ORDER = {ID_ORDER}'
        data = func.query_sql(path_sql, txt, True)
        return cls(*data)

    @staticmethod
    def view_stall_orders(ID_Stall: int, STATUS = False):
        txt = f'SELECT * FROM ORDERS INNER JOIN PRODUCTS USING (ID_PRODUCT) WHERE ID_STALL = {ID_Stall}' + (f" AND STATUS = {STATUS}" * (STATUS))
        data = func.sql_tables(path_sql, txt)
        return data

    @staticmethod
    def view_cart(ID_Customer: int):
        txt = f'SELECT * FROM ORDERS INNER JOIN PRODUCTS USING (ID_PRODUCT) WHERE ID_CUSTOMER = {ID_Customer} AND STATUS = "CARTED";'
        data = func.sql_tables(path_sql, txt)
        return data

    @staticmethod
    def update_order(ID_ORDER: list, STATUS: str):
        for ID_ in ID_ORDER:
            txt = f'UPDATE ORDERS SET STATUS = "{STATUS}" WHERE ID_ORDER = "{ID_}";'
            func.query_sql(path_sql, txt, False)
        return 0

    @staticmethod
    def view_orders(ID_Customer: int):
        txt = f'SELECT ID_ORDER, NAME, PRICE, STATUS, ID_STALL FROM ORDERS INNER JOIN PRODUCTS USING (ID_PRODUCT) WHERE ID_CUSTOMER = {ID_Customer};'
        data = func.sql_tables(path_sql, txt)
        data["COUNTER"] = [func.query_sql(path_sql, f'SELECT COUNT(ID_STALL) AS COUNTER FROM ORDERS INNER JOIN PRODUCTS USING (ID_PRODUCT) WHERE STATUS IN ("PENDING", "PREPARING") GROUP BY ID_STALL HAVING ID_STALL = {ID_STALL} LIMIT 1;', True)[0] for ID_STALL in data["ID_STALL"].values if ID_STALL]
        return data

    @staticmethod
    def cancel_orders(ID_ORDER: list):
        for ID_ in ID_ORDER:
            txt = f'DELETE FROM ORDERS WHERE ID_ORDER = {ID_};'
            func.query_sql(path_sql, txt, False)
        return 0

@dataclass
class Track(object):
    ID_BOX: int
    ID_ORDER: int
    ID_STALL: int
    STATUS: str    # UNOCCUPIED, OCCUPIED

    @staticmethod
    def QUERY(ID_STALL = None):
        if ID_STALL:
            txt = f'SELECT * FROM TRACK WHERE ID_STALL = {ID_STALL};'
            data = func.sql_tables(path_sql, txt)
            return data
        return func.sql_tables(path_sql, f"SELECT * FROM TRACK;")

    @staticmethod
    def QUERY_BOX(ID_BOX: int):
        Q_ID_ORDER = f'SELECT ID_ORDER FROM TRACK WHERE ID_BOX = {ID_BOX};'
        ID_ORDER = func.query_sql(path_sql, Q_ID_ORDER, True)
        if not ID_ORDER:
            return -1
        Q_STATUS = f'SELECT STATUS FROM ORDERS WHERE ID_ORDER = {ID_ORDER[0]}'
        STATUS = func.query_sql(path_sql, Q_STATUS, True)
        if not STATUS:
            return -1
        return f'{STATUS[0]}'

    @staticmethod
    def REGISTER(ID_STALL: int):
        txt = f'INSERT INTO TRACK ID_BOX VALUES (NULL, NULL, {ID_STALL}, "UNOCCUPIED")'
        BOX_ID_Q = f'SELECT ID_BOX FROM TRACK ORDER BY ID_BOX DESC LIMIT 1;'
        func.query_sql(path_sql, txt, False)
        BOX_ID = func.query_sql(path_sql, BOX_ID_Q, True)[0] 
        return BOX_ID

    @staticmethod
    def ALLOCATE(ID_STALL: int):
        txt = f'SELECT ID_BOX FROM TRACK WHERE STATUS = "UNOCCUPIED" AND STALL_ID = {ID_STALL} LIMIT 1 '
        data = func.query_sql(path_sql, txt, True)
        txt_f = f'SELECT ID_ORDER FROM ORDERS WHERE STATUS LIKE "READY" AND STALL_ID = {ID_STALL} LIMIT 1'
        ID_ORDER = func.query_sql(path_sql, txt_f, True)
        if data == None or ID_ORDER == None:
            return -1
        txt_2 = f'UPDATE TRACK SET ID_ORDER = {ID_ORDER[0]}, STATUS = "OCCUPIED" WHERE ID_BOX = {data[0]}'
        func.query_sql(path_sql, txt_2, False)
        return ID_ORDER

    @staticmethod
    def COMPLETE(ID_BOX: int):
        txt = f'UPDATE STATUS = "UNOCCUPIED" WHERE ID_BOX = {ID_BOX}'
        func.query_sql(path_sql, txt, False)
        return 0

class SearchForm(FlaskForm):
    SearchValue = StringField(label="Type Something Here", validators=[DataRequired()])
    submit = SubmitField(label="Search 🔍")

class RegisterForm(FlaskForm):
    Name = StringField(label="UserName", validators=[DataRequired()])
    Phone = StringField(label="Phone Number", validators=[DataRequired()])
    Email = EmailField(label="Email", validators=[DataRequired(), Email()])
    Credit_Card = StringField(label="Credit Card Information", validators=[DataRequired()])
    Password = PasswordField(label="Password", validators=[DataRequired()])
    Password_1 = PasswordField(label="Password", validators=[DataRequired()])
    Submit = SubmitField(label="Submit")

    def validate_Name(self, Name: str):
        res = func.query_sql(path_sql, f"SELECT ID_CUSTOMERS FROM CUSTOMERS WHERE NAME = '{Name}'", True)
        print(res)
        if res != None:
            raise ValidationError("UserName Already Exists...")
        return 0

class LoginForm(FlaskForm):
    Name = StringField(label="UserName", validators=[DataRequired()])
    Password = PasswordField(label="Password", validators=[DataRequired()])
    Submit = SubmitField(label="Login")

    def validate_Password(self, Password: str):
        res = func.query_sql(path_sql, f"SELECT ID_CUSTOMERS FROM CUSTOMERS WHERE NAME = '{self.Name.data}' AND PASSWORD = '{Password.data}';", True)
        print(f"SELECT * FROM CUSTOMERS WHERE NAME = '{self.Name.data}' AND PASSWORD = '{Password.data}';")
        print(res)
        if res == None:
            raise ValidationError("Invalid Username or Password")
        return 0

class PurchaseForm(FlaskForm):
    submit = SubmitField(label="Add to Cart")

class CheckOutForm(FlaskForm):
    submit = SubmitField(label="CheckOut")

class CancelForm(FlaskForm):
    submit = SubmitField(label="Cancel Order")