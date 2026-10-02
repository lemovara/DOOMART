# =========================================================
# DOOMART
# Conexión con SQLite
# =========================================================

import sqlite3
from pathlib import Path


# ---------------------------------------------------------
# UBICACIÓN DE LA BASE DE DATOS
# ---------------------------------------------------------
#
# Path(__file__) representa:
#
# database/db.py
#
# .parent representa:
#
# database/
#
# Entonces creamos:
#
# database/doomart.db
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "doomart.db"


# ---------------------------------------------------------
# CREAR CONEXIÓN
# ---------------------------------------------------------

def get_db():

    # sqlite3.connect() abre nuestra base de datos.
    connection = sqlite3.connect(DATABASE_PATH)

    # sqlite3.Row permite acceder a las columnas
    # por nombre:
    #
    # producto["nombre"]
    #
    # en lugar de:
    #
    # producto[1]
    #
    connection.row_factory = sqlite3.Row

    return connection


# ---------------------------------------------------------
# CERRAR CONEXIÓN
# ---------------------------------------------------------

def close_db(connection):

    if connection is not None:
        connection.close()


# ---------------------------------------------------------
# INICIALIZAR BASE DE DATOS
# ---------------------------------------------------------

def init_db():

    # Abrimos conexión.
    connection = get_db()

    try:

        # Leemos el archivo schema.sql.
        schema_path = BASE_DIR / "schema.sql"

        with open(schema_path, "r", encoding="utf-8") as file:

            schema = file.read()

        # executescript permite ejecutar varias
        # instrucciones SQL.
        connection.executescript(schema)

        # Guardamos cambios.
        connection.commit()

    finally:

        # Siempre cerramos la conexión.
        connection.close()