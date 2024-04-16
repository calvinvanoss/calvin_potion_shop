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
            if barrel.potion_type == [0, 100, 0, 0]:
                connection.execute(
                    sqlalchemy.text(
                        "UPDATE global_inventory SET num_green_ml = num_green_ml + :quantity, gold = gold - :price;"
                    ),
                    {
                        "quantity": barrel.quantity * barrel.ml_per_barrel,
                        "price": barrel.price,
                    },
                )
            elif barrel.potion_type == [0, 0, 100, 0]:
                connection.execute(
                    sqlalchemy.text(
                        "UPDATE global_inventory SET num_blue_ml = num_blue_ml + :quantity, gold = gold - :price;"
                    ),
                    {
                        "quantity": barrel.quantity * barrel.ml_per_barrel,
                        "price": barrel.price,
                    },
                )
            elif barrel.potion_type == [100, 0, 0, 0]:
                connection.execute(
                    sqlalchemy.text(
                        "UPDATE global_inventory SET num_red_ml = num_red_ml + :quantity, gold = gold - :price;"
                    ),
                    {
                        "quantity": barrel.quantity * barrel.ml_per_barrel,
                        "price": barrel.price,
                    },
                )
            else:
                continue

    return "OK"


# Gets called once a day
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):
    """ """
    print(wholesale_catalog)

    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                "SELECT num_green_potions, num_blue_potions, num_red_potions, gold FROM global_inventory LIMIT 1;"
            )
        )

        row = result.fetchone()
        num_green_potions = row[0]
        num_blue_potions = row[1]
        num_red_potions = row[2]
        gold = row[3]

        if (
            num_green_potions <= num_blue_potions
            and num_green_potions <= num_red_potions
        ):
            for barrel in wholesale_catalog:
                if barrel.potion_type == [0, 100, 0, 0]:
                    if gold >= barrel.price:
                        return [
                            {
                                "sku": barrel.sku,
                                "quantity": 1,
                            }
                        ]
        if (
            num_blue_potions <= num_green_potions
            and num_blue_potions <= num_red_potions
        ):
            for barrel in wholesale_catalog:
                if barrel.potion_type == [0, 0, 100, 0]:
                    if gold >= barrel.price:
                        return [
                            {
                                "sku": barrel.sku,
                                "quantity": 1,
                            }
                        ]
        if num_red_potions <= num_green_potions and num_red_potions <= num_blue_potions:
            for barrel in wholesale_catalog:
                if barrel.potion_type == [100, 0, 0, 0]:
                    if gold >= barrel.price:
                        return [
                            {
                                "sku": barrel.sku,
                                "quantity": 1,
                            }
                        ]

    return []
