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
# NOTICIAS
# =========================================================

@app.route("/noticia/<zona>/<int:noticia_id>")
def noticia(zona, noticia_id):

    noticias = {

        "tlaxcala": [

            {
                "id": 1,
                "titulo": "25 Empresas en Tlaxcala Contaminan el Río Zahuapan",
                "imagen": "tlaxcala-1.jpg",
                "texto": """
                Empresas responsables de la contaminación

Según la Comisión Federal para la Protección de Riesgos Sanitarios (Cofepris), estas 25 empresas forman parte de un grupo mayor de 63 empresas que vierten desechos en el río Atoyac-Zahuapan. Este río es uno de los más contaminados del país debido a las descargas ilegales de varias industrias, principalmente de los sectores automotriz, metalmecánico, eléctrico, químico y textil.
Los efectos de la contaminación en la salud

El impacto de la contaminación es alarmante. Las enfermedades infecciosas, así como cánceres y enfermedades renales crónicas, han aumentado en las comunidades cercanas a este afluente. Estos padecimientos están directamente relacionados con la exposición a metales pesados, metaloides, y plaguicidas encontrados en el agua.
El río Atoyac: Un peligro creciente

A lo largo de su recorrido, el río Atoyac es contaminado por 8,000 empresas. Esta contaminación se extiende por varios estados como Tlaxcala, Puebla, Michoacán y Guerrero, hasta desembocar en el Océano Pacífico, llevando con él enormes cantidades de tóxicos que afectan el medio ambiente marino.
Urgente acción para la salud y el medio ambiente

Es esencial que las autoridades y las empresas responsables actúen rápidamente para reducir la contaminación del río Atoyac y proteger tanto la salud de los habitantes como la biodiversidad acuática.
                """
            },

            {
                "id": 2,
                "titulo": "Rescate del Río Atoyac , uno de los más contaminados de México",
                "imagen": "tlaxcala-2.jpg",
                "texto": """
                El Río Atoyac nace en la Sierra Nevada del Estado de Puebla y se extiende a lo largo de 200 kilómetros. 
                Para la primera fase de restauración del Atoyac, la Conagua destinó en Tlaxcala una inversión total de 298.25 millones de pesos . 
                El cuerpo de agua que atraviesa por los estados de Puebla y Tlaxcala, enfrenta una crisis ambiental por las descargas ilegales y la actividad industrial.
                Con los trabajos de rehabilitación, se espera el saneamiento del 15 por ciento de la extensión total del río en los dos próximos años. 
                La Comisión Nacional del Agua ha identificado casi 3 mil descargas ilegales a lo largo del río. 
                El plan de trabajo incluye la construcción de humedales artificiales que también serán una zona de recreación para la población. 
                Los sistemas locales de tratamiento beneficiarán a cerca de 40 mil personas. 
                Dentro de los avances se realizó el inventario del arbolado para la reforestación y la restauración de sus riberas. 
                El plan de saneamiento beneficiará a los ejidatarios al garantizar agua en tiempos de escasez. 
                El plan de recuperación se encuentra en su primera etapa y se estima que con las acciones realizadas los beneficios del saneamiento sean visibles.
                """
            }

        ],


        "mundial": [

            {
                "id": 1,
                "titulo": "Contaminación a nivel mundial",
                "imagen": "mundial-1.jpg",
                "texto": """
                Aquí se colocará el contenido de la noticia
                ambiental mundial.
                """
            },

            {
                "id": 2,
                "titulo": "Problemas ambientales del mundo",
                "imagen": "mundial-2.jpg",
                "texto": """
                Aquí se colocará el contenido de la segunda
                noticia mundial.
                """
            }

        ]

    }


    if zona not in noticias:

        abort(404)


    noticia_encontrada = None


    for item in noticias[zona]:

        if item["id"] == noticia_id:

            noticia_encontrada = item

            break


    if noticia_encontrada is None:

        abort(404)


    return render_template(
        "noticia.html",
        noticia=noticia_encontrada,
        zona=zona
    )

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