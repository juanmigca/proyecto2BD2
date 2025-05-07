


def runCuisinesPipeline(collection):
    """
    Run the cuisines pipeline to update the executive summary collection.
    """
    if collection is None:
        raise ValueError('Collection is None')
    
    pipeline = [
        {
            '$lookup': {
                'from': 'restaurants', 
                'localField': 'name', 
                'foreignField': 'cuisines', 
                'as': 'restaurants'
            }
        }, {
            '$project': {
                '_id': 0, 
                'cuisine': '$name', 
                'total_restaurantes': {
                    '$size': '$restaurants'
                }
            }
        }, {
            '$sort': {
                'total_restaurantes': 1
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
                'tipo': 'Resumen Cuisines', 
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
    ]
    try:
        collection.aggregate(pipeline)
    except Exception as e:
        raise ValueError(f"Error running cuisines pipeline: {e}")


def runIngredientsPipeline(collection):
    if collection is None:
        raise ValueError('Collection is None')
    pipeline = [
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
    ]

    try:
        collection.aggregate(pipeline)
    except Exception as e:
        raise ValueError(f"Error running ingredients pipeline: {e}")
    
def runMenuItemsPipeline(collection):
    if collection is None:
        raise ValueError('Collection is None')
    pipeline = [
        {
            '$lookup': {
                'from': 'restaurants', 
                'localField': 'id', 
                'foreignField': 'menuItems.id', 
                'as': 'restaurants'
            }
        }, {
            '$addFields': {
                'numRestaurantsServedIn': {
                    '$size': '$restaurants'
                }
            }
        }, {
            '$project': {
                '_id': 0, 
                'id': 1, 
                'name': 1, 
                'numRestaurantsServedIn': 1
            }
        }, {
            '$lookup': {
                'from': 'orders', 
                'localField': 'id', 
                'foreignField': 'items.id', 
                'as': 'inOrders'
            }
        }, {
            '$project': {
                'id': 1, 
                'name': 1, 
                'numRestaurantsServedIn': 1, 
                'inOrders': {
                    '$filter': {
                        'input': '$inOrders', 
                        'as': 'orden', 
                        'cond': {
                            '$eq': [
                                '$$orden.status', 'Entregado'
                            ]
                        }
                    }
                }
            }
        }, {
            '$project': {
                'id': 1, 
                'name': 1, 
                'numRestaurantsServedIn': 1, 
                'numOrdersServedIn': {
                    '$size': '$inOrders'
                }, 
                'totalQuantitySold': {
                    '$sum': {
                        '$map': {
                            'input': '$inOrders', 
                            'as': 'orden', 
                            'in': {
                                '$sum': {
                                    '$map': {
                                        'input': {
                                            '$filter': {
                                                'input': '$$orden.items', 
                                                'as': 'item', 
                                                'cond': {
                                                    '$eq': [
                                                        '$$item.id', '$id'
                                                    ]
                                                }
                                            }
                                        }, 
                                        'as': 'matchedItem', 
                                        'in': '$$matchedItem.quantity'
                                    }
                                }
                            }
                        }
                    }
                }, 
                'generatedRevenue': {
                    '$round': [
                        {
                            '$sum': {
                                '$map': {
                                    'input': '$inOrders', 
                                    'as': 'orden', 
                                    'in': {
                                        '$sum': {
                                            '$map': {
                                                'input': {
                                                    '$filter': {
                                                        'input': '$$orden.items', 
                                                        'as': 'item', 
                                                        'cond': {
                                                            '$eq': [
                                                                '$$item.id', '$id'
                                                            ]
                                                        }
                                                    }
                                                }, 
                                                'as': 'matchedItem', 
                                                'in': {
                                                    '$multiply': [
                                                        '$$matchedItem.quantity', '$$matchedItem.price'
                                                    ]
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }, 2
                    ]
                }
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
                'tipo': 'Resumen Menu Items', 
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
    ]
    try:
        collection.aggregate(pipeline)
    except Exception as e:
        raise ValueError(f"Error running menu items pipeline: {e}")
    
def runOrdersPipelines(collection):
    if collection is None:
        raise ValueError('Collection is None')
    pipeline1 = [ #Orders by status
        {
            '$project': {
                'status': 1, 
                'num_items': {
                    '$size': '$items'
                }, 
                'total_quantity': {
                    '$sum': {
                        '$map': {
                            'input': '$items', 
                            'as': 'item', 
                            'in': '$$item.quantity'
                        }
                    }
                }, 
                'subtotal': 1, 
                'tip': 1, 
                'total': 1
            }
        }, {
            '$group': {
                '_id': '$status', 
                'count': {
                    '$sum': 1
                }, 
                'avgItemsPerOrder': {
                    '$avg': '$num_items'
                }, 
                'avgTotalQuantity': {
                    '$avg': '$total_quantity'
                }, 
                'avgSubtotal': {
                    '$avg': '$subtotal'
                }, 
                'avgTip': {
                    '$avg': '$tip'
                }, 
                'avgTotal': {
                    '$avg': '$total'
                }, 
                'sumTotal': {
                    '$sum': '$total'
                }
            }
        }, {
            '$project': {
                '_id': 1, 
                'count': 1, 
                'avgItemsPerOrder': {
                    '$round': [
                        '$avgItemsPerOrder', 2
                    ]
                }, 
                'avgTotalQuantity': {
                    '$round': [
                        '$avgTotalQuantity', 2
                    ]
                }, 
                'avgSubtotal': {
                    '$round': [
                        '$avgSubtotal', 2
                    ]
                }, 
                'avgTip': {
                    '$round': [
                        '$avgTip', 2
                    ]
                }, 
                'avgTotal': {
                    '$round': [
                        '$avgTotal', 2
                    ]
                }, 
                'sumTotal': {
                    '$round': [
                        '$sumTotal', 2
                    ]
                }
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
                'tipo': 'Resumen Órdenes por Status', 
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
    ]
    pipeline2 = [ #General Summary
        {
            '$project': {
                'num_items': {
                    '$size': '$items'
                }, 
                'total_quantity': {
                    '$sum': {
                        '$map': {
                            'input': '$items', 
                            'as': 'item', 
                            'in': '$$item.quantity'
                        }
                    }
                }, 
                'subtotal': 1, 
                'tip': 1, 
                'total': 1
            }
        }, {
            '$group': {
                '_id': None, 
                'count': {
                    '$sum': 1
                }, 
                'avgItemsPerOrder': {
                    '$avg': '$num_items'
                }, 
                'avgTotalQuantity': {
                    '$avg': '$total_quantity'
                }, 
                'avgSubtotal': {
                    '$avg': '$subtotal'
                }, 
                'avgTip': {
                    '$avg': '$tip'
                }, 
                'avgTotal': {
                    '$avg': '$total'
                }, 
                'sumTotal': {
                    '$sum': '$total'
                }
            }
        }, {
            '$project': {
                '_id': 0, 
                'count': 1, 
                'avgItemsPerOrder': {
                    '$round': [
                        '$avgItemsPerOrder', 2
                    ]
                }, 
                'avgTotalQuantity': {
                    '$round': [
                        '$avgTotalQuantity', 2
                    ]
                }, 
                'avgSubtotal': {
                    '$round': [
                        '$avgSubtotal', 2
                    ]
                }, 
                'avgTip': {
                    '$round': [
                        '$avgTip', 2
                    ]
                }, 
                'avgTotal': {
                    '$round': [
                        '$avgTotal', 2
                    ]
                }, 
                'sumTotal': {
                    '$round': [
                        '$sumTotal', 2
                    ]
                }
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
                'tipo': 'Resumen Órdenes', 
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
    ]
    try:
        collection.aggregate(pipeline1)
        collection.aggregate(pipeline2)
    except Exception as e:
        raise ValueError(f"Error running orders pipeline: {e}")
    
def runRestaurantsPipeline(collection):
    if collection is None:
        raise ValueError('Collection is None')
    
    pipeline = [
        {
            '$lookup': {
                'from': 'orders', 
                'localField': 'id', 
                'foreignField': 'restaurantId', 
                'as': 'orders'
            }
        }, {
            '$project': {
                '_id': 0, 
                'id': 1, 
                'name': 1, 
                'menuItems': 1, 
                'orders': {
                    '$filter': {
                        'input': '$orders', 
                        'as': 'order', 
                        'cond': {
                            '$eq': [
                                '$$order.status', 'Entregado'
                            ]
                        }
                    }
                }
            }
        }, {
            '$addFields': {
                'totalOrders': {
                    '$size': '$orders'
                }, 
                'totalRevenue': {
                    '$round': [
                        {
                            '$sum': {
                                '$map': {
                                    'input': '$orders', 
                                    'as': 'order', 
                                    'in': '$$order.total'
                                }
                            }
                        }, 2
                    ]
                }, 
                'totalItemsSold': {
                    '$sum': {
                        '$map': {
                            'input': '$orders', 
                            'as': 'order', 
                            'in': {
                                '$sum': {
                                    '$map': {
                                        'input': '$$order.items', 
                                        'as': 'item', 
                                        'in': '$$item.quantity'
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }, {
            '$addFields': {
                'menuItems': {
                    '$map': {
                        'input': '$menuItems', 
                        'as': 'menuItem', 
                        'in': {
                            'id': '$$menuItem.id', 
                            'name': '$$menuItem.name', 
                            'timesPrepared': {
                                '$sum': {
                                    '$map': {
                                        'input': '$orders', 
                                        'as': 'order', 
                                        'in': {
                                            '$sum': {
                                                '$map': {
                                                    'input': {
                                                        '$filter': {
                                                            'input': '$$order.items', 
                                                            'as': 'item', 
                                                            'cond': {
                                                                '$eq': [
                                                                    '$$item.id', '$$menuItem.id'
                                                                ]
                                                            }
                                                        }
                                                    }, 
                                                    'as': 'matchedItem', 
                                                    'in': '$$matchedItem.quantity'
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }, {
            '$project': {
                'id': 1, 
                'name': 1, 
                'menuItems': 1, 
                'totalOrders': 1, 
                'totalItemsSold': 1, 
                'totalRevenue': 1
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
                'tipo': 'Resumen Restaurantes', 
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
    ]

    try:
        collection.aggregate(pipeline)
    except Exception as e:
        raise ValueError(f"Error running restaurants pipeline: {e}")
    
def runReviewsPipeline(collection):
    if collection is None:
        raise ValueError('Collection is None')
    
    pipeline = [
        {
            '$group': {
                '_id': None, 
                'totalReviews': {
                    '$sum': 1
                }, 
                'avgStars': {
                    '$avg': '$stars'
                }
            }
        }, {
            '$project': {
                '_id': 0, 
                'totalReviews': 1, 
                'avgStars': {
                    '$round': [
                        '$avgStars', 2
                    ]
                }
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
                'tipo': 'Resumen Reviews', 
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
    ]

    try:
        collection.aggregate(pipeline)
    except Exception as e:
        raise ValueError(f"Error running reviews pipeline: {e}")
    

def runUsersPipelines(collection):
    if collection is None:
        raise ValueError('Collection is None')
    
    pipeline1 = [ #Summary by user
        {
            '$lookup': {
                'from': 'orders', 
                'localField': 'id', 
                'foreignField': 'userId', 
                'as': 'orders'
            }
        }, {
            '$lookup': {
                'from': 'reviews', 
                'localField': 'id', 
                'foreignField': 'userId', 
                'as': 'reviews'
            }
        }, {
            '$project': {
                '_id': 0, 
                'id': 1, 
                'username': 1, 
                'completedOrders': {
                    '$size': {
                        '$filter': {
                            'input': '$orders', 
                            'as': 'order', 
                            'cond': {
                                '$eq': [
                                    '$$order.status', 'Entregado'
                                ]
                            }
                        }
                    }
                }, 
                'canceledOrders': {
                    '$size': {
                        '$filter': {
                            'input': '$orders', 
                            'as': 'order', 
                            'cond': {
                                '$eq': [
                                    '$$order.status', 'Cancelado'
                                ]
                            }
                        }
                    }
                }, 
                'totalItems': {
                    '$sum': {
                        '$map': {
                            'input': '$orders', 
                            'as': 'order', 
                            'in': {
                                '$sum': {
                                    '$map': {
                                        'input': '$$order.items', 
                                        'as': 'item', 
                                        'in': '$$item.quantity'
                                    }
                                }
                            }
                        }
                    }
                }, 
                'totalSpent': {
                    '$round': [
                        {
                            '$sum': {
                                '$map': {
                                    'input': '$orders', 
                                    'as': 'order', 
                                    'in': '$$order.total'
                                }
                            }
                        }, 2
                    ]
                }, 
                'avgTip': {
                    '$round': [
                        {
                            '$avg': {
                                '$map': {
                                    'input': '$orders', 
                                    'as': 'order', 
                                    'in': '$$order.tip'
                                }
                            }
                        }, 2
                    ]
                }, 
                'avgStarsGiven': {
                    '$round': [
                        {
                            '$avg': {
                                '$map': {
                                    'input': '$reviews', 
                                    'as': 'review', 
                                    'in': '$$review.stars'
                                }
                            }
                        }, 2
                    ]
                }
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
                'tipo': 'Resumen Por Usuario', 
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
    ]
    pipeline2 = [ #Summary of 'average' user
        {
            '$lookup': {
                'from': 'orders', 
                'localField': 'id', 
                'foreignField': 'userId', 
                'as': 'orders'
            }
        }, {
            '$project': {
                'numOrders': 1, 
                'numReviews': 1, 
                'totalSpent': {
                    '$sum': {
                        '$map': {
                            'input': '$orders', 
                            'as': 'order', 
                            'in': '$$order.total'
                        }
                    }
                }, 
                'avgTip': {
                    '$avg': {
                        '$map': {
                            'input': '$orders', 
                            'as': 'order', 
                            'in': '$$order.tip'
                        }
                    }
                }
            }
        }, {
            '$group': {
                '_id': None, 
                'avgNumOrders': {
                    '$avg': '$numOrders'
                }, 
                'avgNumReviews': {
                    '$avg': '$numReviews'
                }, 
                'avgTotalSpent': {
                    '$avg': '$totalSpent'
                }, 
                'avgTip': {
                    '$avg': '$avgTip'
                }
            }
        }, {
            '$project': {
                '_id': 0, 
                'avgNumOrders': {
                    '$round': [
                        '$avgNumOrders', 2
                    ]
                }, 
                'avgNumReviews': {
                    '$round': [
                        '$avgNumReviews', 2
                    ]
                }, 
                'avgTotalSpent': {
                    '$round': [
                        '$avgTotalSpent', 2
                    ]
                }, 
                'avgTip': {
                    '$round': [
                        '$avgTip', 2
                    ]
                }
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
                'tipo': 'Resumen Usuario Promedio', 
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
    ]

    try:
        collection.aggregate(pipeline1)
        collection.aggregate(pipeline2)
    except Exception as e:
        raise ValueError(f"Error running users pipeline: {e}")
    


def get_formulario(collection, tipo):
    """
    Returns a dictionary with the summary of the specified type.
    """
    if collection is None:
        raise ValueError('Collection is None')
    
    if tipo is None:
        raise ValueError('Tipo is None')
    
    if not isinstance(tipo, str):
        raise ValueError('Tipo must be a string')
    
    if tipo == 'Resumen Ingredientes':
        runIngredientsPipeline(collection)
    elif tipo == 'Resumen Cuisines':
        runCuisinesPipeline(collection)
    elif tipo == 'Resumen Menu Items':
        runMenuItemsPipeline(collection)
    elif tipo == 'Resumen Órdenes por Status' or tipo == 'Resumen Órdenes':
        runOrdersPipelines(collection)
    elif tipo == 'Resumen Restaurantes':
        runRestaurantsPipeline(collection)
    elif tipo == 'Resumen Reviews':
        runReviewsPipeline(collection)
    elif tipo == 'Resumen Por Usuario' or tipo == 'Resumen Usuario Promedio':
        runUsersPipelines(collection)

    resumen = collection.find_one({"tipo": tipo})
    return resumen['contenido']