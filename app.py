from flask import Flask, render_template, abort
from database.db import get_db, init_db

app = Flask(__name__)

init_db()


def dividir_en_slides(productos, cantidad=3):
    return [
        productos[i:i + cantidad]
        for i in range(0, len(productos), cantidad)
    ]


@app.route("/")
def index():
    db = get_db()

    try:
        productos = db.execute(
            """
            SELECT
                productos.id,
                productos.nombre,
                productos.leyenda,
                productos.descripcion,
                productos.imagen,
                productos.etiqueta,
                productos.seccion,
                empresas.nombre AS empresa
            FROM productos
            INNER JOIN empresas
                ON productos.empresa_id = empresas.id
            ORDER BY productos.id
            """
        ).fetchall()

        mas_daninos = [
            producto
            for producto in productos
            if producto["seccion"] == "mas_daninos"
        ]

        pulmones = [
            producto
            for producto in productos
            if producto["seccion"] == "pulmones"
        ]

        slides_mas_daninos = dividir_en_slides(mas_daninos, 3)
        slides_pulmones = dividir_en_slides(pulmones, 3)

        return render_template(
            "index.html",
            slides_mas_daninos=slides_mas_daninos,
            slides_pulmones=slides_pulmones
        )

    finally:
        db.close()


@app.route("/producto/<int:producto_id>")
def producto(producto_id):
    db = get_db()

    try:
        producto = db.execute(
            """
            SELECT
                productos.id,
                productos.nombre,
                productos.leyenda,
                productos.descripcion,
                productos.imagen,
                productos.etiqueta,
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

        if producto is None:
            abort(404)

        return render_template(
            "producto.html",
            producto=producto
        )

    finally:
        db.close()


if __name__ == "__main__":
    app.run(debug=True)