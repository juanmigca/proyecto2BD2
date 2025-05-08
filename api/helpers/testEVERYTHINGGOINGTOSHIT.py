from pymongo import MongoClient

# Requires the PyMongo package.
# https://api.mongodb.com/python/current

client = MongoClient('mongodb+srv://raul:pauwrauw@lab05.yt4up.mongodb.net/?retryWrites=true&w=majority&appName=lab05')
result = client['proyecto2bd']['ingredients'].aggregate([
    {
        '$lookup': {
            'from': 'menuItems', 
            'localField': 'name', 
            'foreignField': 'ingredients.name', 
            'as': 'menuItems'
        }
    }, {
        '$project': {
            '_id': 0, 
            'name': 1, 
            'platillos_usados': {
                '$size': '$menuItems'
            }
        }
    }, {
        '$sort': {
            'platillos_usados': -1
        }
    }, {
        '$group': {
            '_id': None, 
            'contenido': {
                '$push': '$$ROOT'
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'tipo': 'Resumen Ingredientes', 
            'contenido': 1
        }
    }, {
        '$merge': {
            'into': 'Resumenes', 
            'on': 'tipo', 
            'whenMatched': 'merge', 
            'whenNotMatched': 'insert'
        }
    }
])