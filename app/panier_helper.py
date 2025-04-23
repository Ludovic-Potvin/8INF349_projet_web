import os
from redis import Redis
from rq import Queue, Worker

from app.controllers.product_controller import ProductController

DB_REDIS = os.getenv('DB_REDIS')
DB_REDIS_PORT = os.getenv('DB_REDIS_PORT')

redis = Redis.from_url(f'redis://{DB_REDIS}:{DB_REDIS_PORT}')


def get_panier(order_id: int):
    panier_key = f"panier:{order_id}"
    panier_data = redis.hgetall(panier_key)

    products = []
    for product_id, quantity in panier_data.items():
        product, err = ProductController.get_product_by_id(product_id)
        if err == 200:
            product.quantity = int(quantity)
            products.append(product)
    
    return products