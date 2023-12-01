from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'Restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pizzas = db.relationship('Pizza', secondary='restaurant_pizza', backref='Restaurant')

class Pizza(db.Model):
    __tablename__ = 'Pizza'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pizzas = db.relationship('Restaurant', secondary='restaurant_pizza', backref='Pizza')

class RestaurantPizza(db.Model):
    tablename__ = 'Restaurant'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(Restaurant.id), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey(Pizza.id), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Validating the code
def validate_price(self, price):
    return 1 <= price <= 30



# add any models you may need. 