from backend_web import sql, os, UserMixin, dataclass, functions, FlaskForm

class InitializeDataBase(object):
    def __init__(self):
        self.path = os.path.join(os.getcwd(), "storage.db")

    def activate(self):
        from backend_web import functions
        PATH_SQL = self.path
        functions.initialize_customers(PATH_SQL)
        functions.initialize_products(PATH_SQL)
        functions.initialize_stall(PATH_SQL)
        functions.initalize_order(PATH_SQL)
        functions.initialize_track(PATH_SQL)

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
        data = functions.query_sql(f"SELECT * FROM CUSTOMERS WHERE ID = {id_};", True)
        # Cus_Id, Name, Password, Email, Phone, Credit_Card = data
        # return cls(id_, Name, Password, Email, Phone, Credit_Card)
        return cls(*data)

    def register(self):
        functions.query_sql(f"INSERT INTO CUSTOMERS (ID_CUSTOMERS, NAME, PASSWORD, EMAIL, PHONE, CREDIT_CARD) VALUES {self.Cus_ID, self.Name, self.Password, self.Email, self.Phone, self.Credit_Card}", False)
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
        data = functions.query_sql(f"SELECT * FROM CUSTOMERS WHERE ACCOUNT = {Account} AND PASSWORD = {Password};", True)
        return cls(*data)

    def register(self):
        # functions.query_sql(f"INSERT INTO STALL (ID_STALL, NAME, PASSWORD, ACCOUNT, PHONE) VALUES {self.Stall_ID, self.Name, self.Password, self.Account, self.Phone}", False)
        functions.query_sql(f"INSERT INTO STALL (ID_STALL, NAME, PASSWORD, ACCOUNT, PHONE) VALUES {(*vars(self).values(),)}", False)
        return 0