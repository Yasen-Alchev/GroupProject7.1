import csv, os, json, sys, re
from flask import Flask, request, render_template, url_for, redirect, jsonify
from flask_socketio import SocketIO
from datetime import datetime
from json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError



basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_BINDS'] = {'sample_bind': 'sqlite:///sample.db'}

db = SQLAlchemy(app)
db.init_app(app)
socketio = SocketIO(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), unique=False, nullable=True)
    order_number = db.Column(db.Integer, unique=True, nullable=False)
    status = db.Column(db.String(20), unique=False, nullable=False)
    pizzas = db.Column(db.String(100), unique=False, nullable=False)
    drinks = db.Column(db.Text(100), unique=False, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    
    def __repr__(self):
        return f'<Order {self.order_number}, {self.firstname}, {self.lastname},\
            {self.pizzas}, {self.drinks}, {self.status}>'

def get_timestamp():
    return str(datetime.now())

def addOrder(firstname, lastname, email, pizzas, drinks):

    last_record = db.session.query(Order, func.max(Order.order_number)).first()[1]
    if last_record == None:
        last_record = 0
    
    next_order_number = last_record + 1

    order = Order(firstname=firstname, lastname=lastname, email=email,\
        order_number = next_order_number, status="accepted", pizzas=pizzas,\
        drinks=drinks)

    db.session.add(order)
    try:
        db.session.commit()
        print("new order saved in records")
    except SQLAlchemyError as error:
        print(str(error))
        db.session.rollback()

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():

    addOrder("Yasen", "Alchev", 'jd@example.com',\
        "Margarita", '["cola", "fanta"]')
    
    data = Order.query.all()

    return render_template('index.html', data = data)

@app.route('/all')
def getAll():
    orders = Order.query.all()
    print(f"orders = {orders}")
    return render_template('example.html', orders=orders)

@app.route('/register', methods = ['POST'])
def register():

    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    email = request.form.get("email")
    pizzas = request.form.get("pizzas")
    drinks = request.form.get("drinks")

    print(f"{firstname}")
    print(f"{lastname}")
    print(f"{email}")
    print(f"{pizzas}")
    print(f"{drinks}")

    addOrder(firstname, lastname, email, pizzas, drinks)

    return redirect(url_for('getAll'))

@app.route('/login')
def login():
    return render_template("login.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)
    
