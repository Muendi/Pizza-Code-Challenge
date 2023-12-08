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

# Delete a restaurant by ID
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        # Delete associated RestaurantPizzas
        RestaurantPizza.query.filter_by(restaurant_id=id).delete()
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    else:
        return jsonify({"error": "Restaurant not found"}), 404

# Get all pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    formatted_pizzas = [
        {
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }
        for pizza in pizzas
    ]
    return jsonify(formatted_pizzas)

# Route to create a new RestaurantPizza
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.json
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')
    price = data.get('price')

    if not (pizza_id and restaurant_id and price):
        return jsonify({"errors": ["Please provide pizza_id, restaurant_id, and price"]}), 400
# Check if both Pizza and Restaurant exist
    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not (pizza and restaurant):
        return jsonify({"errors": ["Pizza or Restaurant not found"]}), 404

    # Create RestaurantPizza
    try:
        new_restaurant_pizza = RestaurantPizza(
            pizza_id=pizza_id,
            restaurant_id=restaurant_id,
            price=price
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        return jsonify({
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 500

if __name__ == '__main__':
    app.run(port=5555)
