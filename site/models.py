from email.policy import default
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    email = db.Column(db.String(100), nullable=True, unique=True)
    password = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(1000), nullable=False, unique=False)
    orders = db.relationship("Order", backref="user")

    def __repr__(self) -> str:
        return f"<User:\n" + \
            f"\tid: {self.id}\n" + \
            f"\temail: {self.email}\n" + \
            f"\tpassword: {self.password}\n" + \
            f"\tname: {self.name}\n" + \
            f"\torders: {self.orders}\n>" 

class Order(UserMixin, db.Model):
    id = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    order_number = db.Column(db.Integer, unique=True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    pizzas = db.relationship("Pizza", backref="order")
    completed = db.Column(db.Integer, nullable=False, default=0)

    def toJson(self):
        return {
            "id": f"{self.id}",
            "order_number": f"{self.order_number}",
            "user_id": f"{self.user_id}",
            # "pizzas": f"{self.pizzas}",
            "completed": f"{self.completed}"
        }

    def __repr__(self) -> str:
        return f"\n\n<Order:\n" + \
            f"\torder_number: {self.order_number}\n" + \
            f"\tuser_id: {self.user_id}\n" + \
            f"\tpizzas: {self.pizzas}\n" + \
            f"\tcompleted: {self.completed}\n>" 

class Pizza(UserMixin, db.Model):
    id = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable = False)
    price = db.Column(db.Integer, nullable=False)
    ingridients = db.Column(db.Text)
    alergies = db.Column(db.Text)
    modifications = db.Column(db.Text)
    pizza_count = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable = False)

    def __repr__(self) -> str:
        return f"\n\n<Pizza:\n" + \
            f"\tid: {self.id}\n" + \
            f"\tname: {self.name}\n" + \
            f"\tprice: {self.price}\n" + \
            f"\tingridients: {self.ingridients}\n" + \
            f"\talergies: {self.alergies}\n" + \
            f"\tmodifications: {self.modifications}\n" + \
            f"\tpizza_count: {self.pizza_count}\n" + \
            f"\torder_id: {self.order_id}\n>" 
