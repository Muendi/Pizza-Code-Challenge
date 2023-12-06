#!/usr/bin/env python3

from flask import Flask, jsonify, request #make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

# Route to get all restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    formatted_restaurants = [
        {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address
        }
        for restaurant in restaurants
    ]
    return jsonify(formatted_restaurants)

# Route to get a specific restaurant by ID
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        pizzas = [
            {
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients
            }
            for pizza in restaurant.pizzas
        ]
        restaurant_data = {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "pizzas": pizzas
        }
        return jsonify(restaurant_data)
    else:
        return jsonify({"error": "Restaurant not found"}), 404


if __name__ == '__main__':
    app.run(port=5555)
