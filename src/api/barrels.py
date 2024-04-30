from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/barrels",
    tags=["barrels"],
    dependencies=[Depends(auth.get_api_key)],
)


class Barrel(BaseModel):
    sku: str

    ml_per_barrel: int
    potion_type: list[int]
    price: int

    quantity: int


@router.post("/deliver/{order_id}")
def post_deliver_barrels(barrels_delivered: list[Barrel], order_id: int):
    """ """
    print(f"barrels delievered: {barrels_delivered} order_id: {order_id}")

    with db.engine.begin() as connection:
        for barrel in barrels_delivered:
            connection.execute(
                sqlalchemy.text(
                    f"""
                    INSERT INTO global_inventory (red_ml, green_ml, blue_ml, gold, description) VALUES (
                    {barrel.potion_type[0] * barrel.quantity * barrel.ml_per_barrel},
                    {barrel.potion_type[1] * barrel.quantity * barrel.ml_per_barrel},
                    {barrel.potion_type[2] * barrel.quantity * barrel.ml_per_barrel},
                    {-barrel.price},
                    'Barrel order {order_id}: {barrel.sku} delivered');
                    """
                ),
            )

    return "OK"


# Gets called once a day
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):
    """ """
    print(wholesale_catalog)

    with db.engine.begin() as connection:
        inventory = connection.execute(
            sqlalchemy.text(
                "SELECT SUM(red_ml), SUM(green_ml), SUM(blue_ml), SUM(gold) FROM global_inventory;"
            )
        ).fetchone()

        red_ml = inventory[0]
        green_ml = inventory[1]
        blue_ml = inventory[2]
        gold = inventory[3]

        if green_ml <= blue_ml and green_ml <= red_ml:
            for barrel in wholesale_catalog:
                if barrel.potion_type == [0, 1, 0, 0]:
                    if gold >= barrel.price:
                        return [
                            {
                                "sku": barrel.sku,
                                "quantity": 1,
                            }
                        ]
        if blue_ml <= green_ml and blue_ml <= red_ml:
            for barrel in wholesale_catalog:
                if barrel.potion_type == [0, 0, 1, 0]:
                    if gold >= barrel.price:
                        return [
                            {
                                "sku": barrel.sku,
                                "quantity": 1,
                            }
                        ]
        if red_ml <= green_ml and red_ml <= blue_ml:
            for barrel in wholesale_catalog:
                if barrel.potion_type == [1, 0, 0, 0]:
                    if gold >= barrel.price:
                        return [
                            {
                                "sku": barrel.sku,
                                "quantity": 1,
                            }
                        ]

    return []
