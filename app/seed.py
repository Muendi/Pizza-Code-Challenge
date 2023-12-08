from app import app, db, Restaurant, Pizza, RestaurantPizza

def seed_data():
    with app.app_context():
        restaurants_data = [
            {"name": "Restaurant 1", "address": "123 Main St"},
            {"name": "Restaurant 2", "address": "456 Elm St"}
        ]

        pizzas_data = [
            {"name": "Cheese Pizza", "ingredients": "Dough, Tomato Sauce, Cheese"},
            {"name": "Pepperoni Pizza", "ingredients": "Dough, Tomato Sauce, Cheese, Pepperoni"}
        ]
        
        # Dictionary mapping between restaurants and pizzas
        restaurant_pizzas_data = [
            {"restaurant_id": 1, "pizza_id": 1, "price": 10},
            {"restaurant_id": 1, "pizza_id": 2, "price": 12},
            {"restaurant_id": 2, "pizza_id": 1, "price": 11}
        ]

        for restaurant_data in restaurants_data:
            new_restaurant = Restaurant(**restaurant_data)
            db.session.add(new_restaurant)
        
        for pizza_data in pizzas_data:
            new_pizza = Pizza(**pizza_data)
            db.session.add(new_pizza)
        
        for association_data in restaurant_pizzas_data:
            new_association = RestaurantPizza(**association_data)
            db.session.add(new_association)
        
        db.session.commit()

if __name__ == "__main__":
    seed_data()
