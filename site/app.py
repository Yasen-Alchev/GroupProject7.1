import csv, os, json, sys, re
from flask import Flask, request, render_template, url_for, redirect
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

db = SQLAlchemy(app)
socketio = SocketIO(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Order {self.firstname}>'

def get_timestamp():
    return str(datetime.now())

@app.route('/')
def index():
    student_john = Order(firstname='john', lastname='doe',
                       email='jd@example.com', age=23,
                       bio='Biology student')

    db.session.add(student_john)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        print(str(e))
        db.session.rollback()

    return render_template('index.html', data=student_john)

@app.route('/all')
def getAll():
    orders = Order.query.all()
    print(f"orders = {orders}")
    return render_template('example.html', orders=orders)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
    
