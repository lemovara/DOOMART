from flask import Flask, render_template, abort, request, jsonify
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


        slides_mas_daninos = dividir_en_slides(
            mas_daninos,
            3
        )


        slides_pulmones = dividir_en_slides(
            pulmones,
            3
        )


        return render_template(
            "index.html",
            slides_mas_daninos=slides_mas_daninos,
            slides_pulmones=slides_pulmones
        )


    finally:

        db.close()


# =========================================================
# DETALLE DE PRODUCTO
# =========================================================

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


# =========================================================
# GENERAR TICKET
# =========================================================

@app.route("/api/ticket", methods=["POST"])
def generar_ticket():

    data = request.get_json(silent=True)


    if not data:

        return jsonify({
            "ok": False,
            "error": "No se recibieron datos."
        }), 400


    productos_ids = data.get("productos", [])


    if not isinstance(productos_ids, list):

        return jsonify({
            "ok": False,
            "error": "Formato de productos inválido."
        }), 400


    if len(productos_ids) == 0:

        return jsonify({
            "ok": False,
            "error": "El DOOMCART está vacío."
        }), 400


    if len(productos_ids) > 5:

        return jsonify({
            "ok": False,
            "error": "El máximo es de 5 productos."
        }), 400


    try:

        productos_ids = [
            int(producto_id)
            for producto_id in productos_ids
        ]

    except (ValueError, TypeError):

        return jsonify({
            "ok": False,
            "error": "Uno de los productos no es válido."
        }), 400


    db = get_db()

    try:

        placeholders = ",".join(
            "?"
            for _ in productos_ids
        )


        productos = db.execute(
            f"""
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

            WHERE productos.id IN ({placeholders})

            ORDER BY productos.id
            """,
            productos_ids
        ).fetchall()


        if not productos:

            return jsonify({
                "ok": False,
                "error": "No se encontraron los productos."
            }), 404


        ticket = []


        for producto in productos:

            ticket.append({

                "id": producto["id"],

                "nombre": producto["nombre"],

                "empresa": producto["empresa"],

                "etiqueta": producto["etiqueta"],

                "leyenda": producto["leyenda"],

                "descripcion": producto["descripcion"],

                "imagen": producto["imagen"],

                "empresa_descripcion":
                    producto["empresa_descripcion"],

                "caracteristicas":
                    producto["caracteristicas"],

                "danio_suelo":
                    producto["danio_suelo"],

                "danio_aire":
                    producto["danio_aire"],

                "danio_agua":
                    producto["danio_agua"],

                "uso_recursos":
                    producto["uso_recursos"],

                "plasticos_residuos":
                    producto["plasticos_residuos"],

                "fuente":
                    producto["fuente"]

            })


        return jsonify({

            "ok": True,

            "cantidad": len(ticket),

            "productos": ticket

        })


    finally:

        db.close()


# =========================================================
# EJECUTAR
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )