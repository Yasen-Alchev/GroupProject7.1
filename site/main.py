from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Order, Pizza
from sqlalchemy import func 
from . import db
import json

main = Blueprint('main', __name__)

def update_session_cart():
    if session.get("cart") == None:
        session["cart"] = {}
    set_session_user()
    current_order = Order.query.filter_by(user_id = session["UserID"], completed = 0).first()
    
    if current_order:
        cart = {}
        for pizza in current_order.pizzas:
            if pizza.name in cart:
                cart[pizza.name]["count"] += 1
                cart[pizza.name]["price"] += pizza.price
                cart[pizza.name]["price"] = round(cart[pizza.name]["price"], 2)
            else:
                cart[pizza.name] = {}
                cart[pizza.name]["count"] = 1
                cart[pizza.name]["price"] = round(pizza.price, 2)
            if not "total" in cart:
                cart["total"] = 0.0
            cart["total"] += pizza.price
            cart["total"] = round(cart["total"], 2)

        session["cart"] = cart
        print(f"cart = {cart}")


def set_session_user():
    if session.get("UserID") == None or User.query.filter_by(id = session["UserID"]).first() == None:
        if current_user.is_authenticated:
            session["UserID"] = current_user.id
        else:
            user = User(name="TempUser")
            db.session.add(user)
            db.session.commit()
            session["UserID"] = user.id
        print(f"user with ID: {session['UserID']} created")

@main.route('/')
def index():
    update_session_cart()
    print(f'session["cart"] = {session["cart"]}')
    return render_template('index.html', cart=session["cart"])

@main.route('/add_pizza', methods=["POST"])
def add_pizza():
    data = request.get_json()
    print(f"Adding Pizza: {data}")

    order_ids = Order.query.filter_by(order_number = Order.order_number).all()
    order_ids = [order.id for order in order_ids]
    if order_ids:
        next_order_number = max(order_ids) + 1
        print(f"next_order_number = {next_order_number}")
    else:
        print("No orders registred in the database yet!")
        next_order_number = 1

    user = User.query.filter_by(id = session["UserID"]).first()

    current_order = Order.query.filter_by(user_id = user.id, completed = 0).first()
    if not current_order:
            current_order = Order(order_number = next_order_number, user_id = user.id, completed = False)
            db.session.add(current_order)        
            db.session.commit()

    new_pizza = Pizza(name=data["pizza_name"], price= data["price"], ingridients="", alergies="", modifications="", pizza_count=1, order_id = current_order.id)
    db.session.add(new_pizza)
    db.session.commit()

    update_session_cart()
    
    return session["cart"]

@main.route('/profile')
@login_required
def profile():

    # print(f"Orders: {Order.query.all()}")

    return render_template('profile.html', name=current_user.name)

@main.route('/tracker')
def tracker():
    return render_template('tracker.html')

@main.route('/remove_item', methods=["POST"])
def remove_item():
    item = request.get_json()

    current_order = Order.query.filter_by(user_id = session["UserID"], completed = 0).first()
    delete_q = Pizza.__table__.delete().where(Pizza.order_id == current_order.id, Pizza.name == item['name'])

    db.session.execute(delete_q)
    db.session.commit()

    update_session_cart()
    if "total" in session["cart"]:
        total = session["cart"]["total"]
    else:
        total = "0.00"

    return {"total" : total}


