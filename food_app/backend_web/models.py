from backend_web import sql, os, UserMixin, dataclass, functions

@dataclass
class Customers(UserMixin):
    def __init__(self, CusId):
        Cus_Id: int
        Name: str
        Password: str
        Email: str
        Phone: str
        Credit_Card: str
        
    @classmethod
    def retrieve_person(cls: object, id_: int):
        data = functions.query_sql(f"SELECT FROM CUSTOMERS WHERE ID = {id_};", True)
        Cus_Id, Name, Password, Email, Phone, Credit_Card = data
        return cls(id_, Name, Password, Email, Phone, Credit_Card)