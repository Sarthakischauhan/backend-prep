from fastapi import FastAPI
import redis
from db import DB
from interfaces import Order

app = FastAPI()
DATABASE_URI = "postgresql://user:password@localhost:5432/interview_prep"

# A simple class for all db related operations
db = DB()
# Initialise a connection and a cursor object
db.connect()
db.create_tables()

@app.post("/add-orders")
def create_order(order: Order):
    columns = ["user_id", "vehicle_id"]
    values = [order.user_id, order.vehicle_id] 
    db.insert_data("orders", columns, values)

@app.get("/table_exists/{table_name}")
def table_exists(table_name:str):
    return db.check_table(table_name)

@app.get("/get-orders/{order_id}")
def get_orders(order_id:int):
    return {"order_id":order_id}
