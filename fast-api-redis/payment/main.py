from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request

import requests
import time
import json

secrets = json.loads(open('../secret.json').read())

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)


redis = get_redis_connection(
    host=secrets['redis']['host'],
    port=secrets['redis']['port'],
    password=secrets['redis']['password'],
    decode_responses=True
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str

    class Meta:
        database = redis


@app.get('/orders/{pk}')
def get(pk: str):
    order = Order.get(pk)
    redis.xadd('refund_order', order.dict(), '*')
    return order


@app.post('/orders')
async def create(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()

    req = requests.get(f"http://localhost:8000/products/{body['id']}")
    product = req.json()
    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=.2*product['price'],
        total=1.2*product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()
    background_tasks.add_task(order_completed, order)
    return order


def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), "*")
