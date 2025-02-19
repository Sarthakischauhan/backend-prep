from pydantic import BaseModel

class Order(BaseModel):
    user_id: int 
    vehicle_id: int