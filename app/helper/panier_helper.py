import os
from redis import Redis
import uuid
from flask import request, g

from app.controllers.product_controller import ProductController

DB_REDIS = os.getenv('REDIS')
DB_REDIS_PORT = os.getenv('REDIS_PORT')

redis_url = f"redis://{DB_REDIS}:{DB_REDIS_PORT}/0"
redis = Redis.from_url(redis_url)

def set_panier_redis(cart_id):
    redis.expire(f"panier:{cart_id}", 3600)

def get_panier_redis():
    panier_id = g.cart_id

    panier_key = f"panier:{panier_id}"
    panier_data = redis.hgetall(panier_key)
    products = []
    for product_id, quantity in panier_data.items():
        product_id = int(product_id.decode())
        quantity = int(quantity.decode())
        print(product_id)
        product = ProductController.get_product_by_id(product_id)
        product.quantity = int(quantity)
        products.append(product)
    return products

def add_product_to_cart(product_id, quantity):
    panier_id = g.cart_id
    current_qty = redis.hget(panier_id, product_id)
    print(current_qty)
    new_qty = int(current_qty or 0) + quantity
    print(new_qty)
    cart_key = f"panier:{panier_id}"
    redis.hset(cart_key, product_id, new_qty)

    redis.expire(panier_id, 3600)

    print(f"Added {quantity} of {product_id} to cart {panier_id}")
    return True

def unset_panier_redis():
    panier_id = g.cart_id
    redis.delete(f"panier:{panier_id}")
