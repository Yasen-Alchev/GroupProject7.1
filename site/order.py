# from app import db, func

# class Order(db.Model):
#     __bind_key__ = 'sample_bind'
#     __tablename__ = "Order"

#     id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(50), nullable=True)
#     lastname = db.Column(db.String(50), nullable=True)
#     email = db.Column(db.String(30), unique=True, nullable=True)
#     order_number = db.Column(db.Integer, unique=True, nullable=False)
#     status = db.Column(db.String(20), unique=False, nullable=False)
#     pizzas = db.Column(db.Text(100), unique=False, nullable=False)
#     drinks = db.Column(db.Text(100), unique=False, nullable=True)
#     created_at = db.Column(db.DateTime(timezone=True),
#                            server_default=func.now())
    
#     def __repr__(self):
#         return f'<Order {self.order_number}, {self.firstname}, {self.lastname},\
#             {self.pizza_name}, {self.drinks}, {self.status}>'