# =========================================================
# DOOMART
# Aplicación principal Flask
# =========================================================

from flask import Flask, render_template, abort

from database.db import get_db, init_db


# =========================================================
# CREAR APLICACIÓN
# =========================================================

app = Flask(__name__)


# =========================================================
# INICIALIZAR BASE DE DATOS
# =========================================================
#
# Al arrancar la aplicación:
#
# - si la base no existe, SQLite la crea
# - se crean las tablas
#
# =========================================================

init_db()


# =========================================================
# RUTA PRINCIPAL
# =========================================================

@app.route("/")
def index():

    # -----------------------------------------
    # Abrir conexión
    # -----------------------------------------

    db = get_db()

    try:

        # -----------------------------------------
        # Obtener todos los productos
        # -----------------------------------------

        productos = db.execute(
            """
            SELECT
                productos.id,
                productos.nombre,
                productos.leyenda,
                productos.descripcion,
                productos.imagen,
                empresas.nombre AS empresa

            FROM productos

            INNER JOIN empresas
                ON productos.empresa_id = empresas.id

            ORDER BY productos.id
            """
        ).fetchall()

        # -----------------------------------------
        # Enviar los productos al HTML
        # -----------------------------------------

        return render_template(
            "index.html",
            productos=productos
        )

    finally:

        # -----------------------------------------
        # Cerrar SQLite
        # -----------------------------------------

        db.close()


# =========================================================
# RUTA PARA UN PRODUCTO ESPECÍFICO
# =========================================================
#
# Ejemplo:
#
# /producto/1
#
# /producto/2
#
# /producto/3
#
# =========================================================

@app.route("/producto/<int:producto_id>")
def producto(producto_id):

    db = get_db()

    try:

        # Buscar producto + empresa asociada.

        producto = db.execute(
            """
            SELECT

                productos.id,
                productos.nombre,
                productos.leyenda,
                productos.descripcion,
                productos.imagen,

                empresas.id AS empresa_id,
                empresas.nombre AS empresa,
                empresas.descripcion AS empresa_descripcion,
                empresas.caracteristicas,
                empresas.danio_suelo,
                empresas.danio_aire,
                empresas.danio_agua,
                empresas.uso_recursos,
                empresas.plasticos_residuos,
                empresas.fuente

            FROM productos

            INNER JOIN empresas
                ON productos.empresa_id = empresas.id

            WHERE productos.id = ?

            """,
            (producto_id,)
        ).fetchone()


        # -----------------------------------------
        # Si no existe
        # -----------------------------------------

        if producto is None:

            abort(404)


        # -----------------------------------------
        # Mostrar página
        # -----------------------------------------

        return render_template(
            "producto.html",
            producto=producto
        )

    finally:

        db.close()


# =========================================================
# EJECUTAR SERVIDOR
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )