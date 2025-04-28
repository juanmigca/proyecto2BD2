import random
from datetime import datetime, timedelta
import json

def gen_fecha_rand():
    year = random.randint(2015, 2025)
    month = random.randint(1, 12)
    if month <=9:
        month = "0" + str(month)
    day = random.randint(1, 28)
    if day <=9:
        day = "0" + str(day)
    return str(year) + "-" + str(month) + "-" + str(day)

def gen_fecha_hora_rand():
    year = random.randint(2015, 2025)
    month = random.randint(1, 12)
    if month <=9:
        month = "0" + str(month)
    day = random.randint(1, 28)
    if day <=9:
        day = "0" + str(day)
    hour = random.randint(8, 20)
    if hour <=9:
        hour = "0" + str(hour)
    minute = random.randint(0, 59)
    if minute <=9:
        minute = "0" + str(minute)
    return str(year) + "-" + str(month) + "-" + str(day) + "T" + str(hour) + ":" + str(minute) + ":00"

def generate_ingredients(num_ingredients):
    ingredients = []

    for i in range(num_ingredients):
        ingredient = {
            'name': f'Ingrediente {i + 1}',
            'unitMeasure': random.choice(['g', 'kg', 'l', 'ml', 'unidades', 'tbsp']),
        }
        if ingredient['unitMeasure'] == 'g' or ingredient['unitMeasure'] == 'ml':
            ingredient['amount'] = round(random.uniform(100, 1000), 0)
        elif ingredient['unitMeasure'] == 'kg' or ingredient['unitMeasure'] == 'l':
            ingredient['amount'] = round(random.uniform(1, 10), 2)
        else:
            ingredient['amount'] = round(random.uniform(1, 10), 0)
        ingredients.append(ingredient)
    return ingredients

def generate_menu_items(num_items):
    menu_items = []
    ingredientes = generate_ingredients(30)

    for i in range(num_items):
        item = {
            'id': i + 1,
            'name': f'Plato {i + 1}',
            'price': round(random.uniform(5.0, 50.0), 2),
            'ingredients': random.sample(ingredientes, random.randint(1, 5)),
            'addedToMenu': gen_fecha_rand()
            
        }
        menu_items.append(item)
    return menu_items

def generate_restaurants(num_restaurants, menuItems):
    restaurants = []
    cuisines = ['Italiana', 'Mexicana', 'China', 'Japonesa', 'Española', 'India','Americana', 'Guatemalteca', 'Francesa', 'Tailandesa', 'Vietnamita', 'Coreana', 'Mediterránea', 'Griega', 'Turca']
    for i in range(num_restaurants):
        restaurant = {
            'id': i + 1,
            'name': f'Restaurante {i + 1}',
            'cuisines': random.sample(cuisines, random.randint(1, 3)),
            'address': 'Calle ' + str(random.randint(1, 100)) + ', Avenida '+str(random.randint(1, 100))+', Ciudad ' + str(random.randint(1, 10)),
            'location':{
                'type': 'Point',
                'coordinates': [round(random.uniform(-90.0, 90.0), 6), round(random.uniform(-180.0, 180.0), 6)]
            },
            'menuItems': random.sample(menuItems, 40)
        }
        restaurants.append(restaurant)
    return restaurants


def generate_users_orders_reviews(num_users, restaurants):
    users = []
    orders = []
    reviews = []
    for i in range(num_users):
        user = {
            'id': i+1,
            'username': f'usuario{i+1}',
            'numOrders': random.randint(15,30),
            'numReviews':random.randint(0,4),
            'visitedRestaurants': [x['id'] for x in random.sample(restaurants, random.randint(1, 5))]
        }
        users.append(user)
        current_user_orders = []
        for j in range(user['numOrders']):
            restaurant_ordered = random.choice(user['visitedRestaurants'])
            restaurant_temp = [x for x in restaurants if x['id'] == restaurant_ordered][0]
            order = {
                'id': len(orders) + 1,
                'userId': user['id'],
                'orderedAt': gen_fecha_hora_rand(),
                'arrivedAt': None,
                'status': random.choices(['Entregado', 'En camino', 'Cancelado'], weights=[0.8, 0.05, 0.15])[0],
                'restaurantId': restaurant_ordered,
                'items': random.sample(restaurant_temp['menuItems'], random.randint(1, 5))
            }
            order['subtotal'] = round(sum(item['price'] for item in order['items']),2)
            order['tax'] = round(order['subtotal'] * 0.12, 2)
            order['tip'] = round(order['subtotal'] * random.uniform(0.05, 0.2), 2)
            order['total'] = round(order['subtotal'] + order['tax'] + order['tip'], 2)
            if order['status'] == 'Entregado':
                order['arrivedAt'] = (datetime.strptime(order['orderedAt'], "%Y-%m-%dT%H:%M:%S") + timedelta(minutes=random.randint(30, 120))).strftime("%Y-%m-%dT%H:%M:%S")
            orders.append(order)
            current_user_orders.append(order)
        for j in range(user['numReviews']):
            to_review = random.choice(['restaurant', 'order'])
            extracted_order = random.choice(current_user_orders)
            current_user_orders.remove(extracted_order)
            if to_review == 'restaurant':
                review = {
                    'id': len(reviews) + 1,
                    'userId': user['id'],
                    'restaurantId': extracted_order['restaurantId'],
                    'stars': random.randint(1, 10),
                    'comment': None,
                    'timestamp': (datetime.strptime(extracted_order['orderedAt'], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=random.randint(8, 24))).strftime("%Y-%m-%dT%H:%M:%S")
                }
                if review['stars'] <= 3:
                    review['comment'] = random.choice(['Mal restaurante', 'No lo recomiendo', 'Pésimo servicio', 'No volveré a pedir aquí'])
                elif review['stars']>3 and review['stars'] <= 7:
                    review['comment'] = random.choice(['Comida regular', 'No estuvo mal', 'Puede mejorar'])
                elif review['stars']>7:
                    review['comment'] = random.choice(['Excelente restaurante', 'Muy buen servicio', 'Recomendado', 'Volveré a pedir aquí'])
            else:
                review = {
                    'id': len(reviews) + 1,
                    'userId': user['id'],
                    'orderId': extracted_order['id'],
                    'restaurantId': extracted_order['restaurantId'],
                    'stars': random.randint(1, 10),
                    'comment': None,
                    'timestamp': (datetime.strptime(extracted_order['orderedAt'], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=random.randint(8, 24))).strftime("%Y-%m-%dT%H:%M:%S")
                }
                if review['stars'] <= 3:
                    review['comment'] = random.choice(['Mal pedido', 'Comida venía mal preparada', 'Sabía muy mal', 'Faltaban productos'])
                elif review['stars']>3 and review['stars'] <= 7:
                    review['comment'] = random.choice(['Comida regular', 'No estuvo mal', 'Puede mejorar', 'La mayoría supo bien, pero hubo un par de cosas que no me gustaron'])
                elif review['stars']>7:
                    review['comment'] = random.choice(['Seguro volveré a pedir estos platillos del menú', 'Todo sabía riquísimo', 'Recomendado', 'Orden completa y buena presentación'])
            reviews.append(review)
    return users, orders, reviews


def generate_cuisines():
    names = ['Italiana', 'Mexicana', 'China', 'Japonesa', 'Española', 'India','Americana', 'Guatemalteca', 'Francesa', 'Tailandesa', 'Vietnamita', 'Coreana', 'Mediterránea', 'Griega', 'Turca']
    cuisines = []
    for i in range(len(names)):
        cuisine = {
            'id': i+1,
            'name': f'{names[i]}',
            'description': f'Descripción de la cocina {names[i]}',
            'created_at': gen_fecha_rand()
        }
        cuisines.append(cuisine)
    return cuisines

def addRestaurantRatings(restaurants, reviews):
    """
    Adds ratings to restaurants based on reviews.
    """
    for restaurant in restaurants:
        restaurant['rating'] = 0
        restaurant['numReviews'] = 0
        for review in reviews:
            try: 
                restIdReview = review['restaurantId']
            except:
                continue
            if review['restaurantId'] == restIdReview:
                restaurant['rating'] += review['stars']
                restaurant['numReviews'] += 1
        if restaurant['numReviews'] > 0:
            restaurant['rating'] /= restaurant['numReviews']
    return restaurants


"""main"""

menu_items = generate_menu_items(300)

with open('menu_items.json', 'w') as f:
    json.dump(menu_items, f)
print("Menu items generated and saved")
restaurants = generate_restaurants(50, menu_items)


users, orders, reviews = generate_users_orders_reviews(2500, restaurants)

with open('users.json', 'w') as f:
    json.dump(users, f)
print("Users generated and saved")
with open('orders.json', 'w') as f:
    json.dump(orders, f)
print("Orders generated and saved")
with open('reviews.json', 'w') as f:
    json.dump(reviews, f)
print("Reviews generated and saved")

cuisines = generate_cuisines()
with open('cuisines.json', 'w') as f:
    json.dump(cuisines, f)
print("Cuisines generated and saved")

restaurants = addRestaurantRatings(restaurants, reviews)

with open('restaurants.json', 'w') as f:
    json.dump(restaurants, f)
print("Restaurants generated and saved")
    