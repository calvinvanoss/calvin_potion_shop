from fastapi import APIRouter
import sqlalchemy
from src import database as db

router = APIRouter()


@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    """
    Each unique item combination must have only a single price.
    """
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT * FROM global_inventory ORDER BY created_at DESC LIMIT 1;"))

    if result.fetchone()[2] > 0:
        return [
            {
                "sku": "GREEN_POTION_0",
                "name": "green potion",
                "quantity": 1,
                "price": 50,
                "potion_type": [0, 100, 0, 0],
            }
        ]
    return []
