import os
import dotenv
from sqlalchemy import create_engine, text

def database_connection_url():
    dotenv.load_dotenv()
    return os.environ.get("POSTGRES_URI")

def validate_connection(engine):
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return result.scalar() == 1

engine = create_engine(database_connection_url(), pool_pre_ping=True)

if validate_connection(engine):
    print("Connection to the database is successful.")
else:
    print("Failed to connect to the database.")