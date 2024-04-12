from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/bottler",
    tags=["bottler"],
    dependencies=[Depends(auth.get_api_key)],
)

class PotionInventory(BaseModel):
    potion_type: list[int]
    quantity: int

@router.post("/deliver/{order_id}")
def post_deliver_bottles(potions_delivered: list[PotionInventory], order_id: int):
    """ """
    print(f"potions delievered: {potions_delivered} order_id: {order_id}")

    with db.engine.begin() as connection:
        for potion in potions_delivered:
            connection.execute(sqlalchemy.text("UPDATE global_inventory SET num_green_potions = num_green_potions + :potion_quantity, num_green_ml = num_green_ml - :ml_quantity;"), potion.quantity, potion.quantity * 100)

    return "OK"

@router.post("/plan")
def get_bottle_plan():
    """
    Go from barrel to bottle.
    """

    # Each bottle has a quantity of what proportion of red, blue, and
    # green potion to add.
    # Expressed in integers from 1 to 100 that must sum up to 100.

    # Initial logic: bottle all barrels into red potions.

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT * FROM global_inventory ORDER BY created_at DESC LIMIT 1;"))

        green_ml = result.fetchone()[3]
        bottled_quantity = green_ml // 100

        connection.execute(sqlalchemy.text("UPDATE global_inventory SET ml_in_barrels = num_green_ml - :bottled_quantity;"), bottled_quantity)

        return [
            {
                "potion_type": [0, 100, 0, 0],
                "quantity": bottled_quantity,
            }
        ]
    
    

if __name__ == "__main__":
    print(get_bottle_plan())