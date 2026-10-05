import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "doomart.db"


def get_db():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection
#para que no salgan como listas simples y salga 

def close_db(connection):
    if connection is not None:
        connection.close()


def init_db():
    connection = get_db()

    try:
        schema_path = BASE_DIR / "schema.sql"

        with open(schema_path, "r", encoding="utf-8") as file:
            schema = file.read()

        connection.executescript(schema)
        connection.commit()

    finally:
        connection.close()