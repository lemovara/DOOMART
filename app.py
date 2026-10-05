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
                "titulo": "Residuos plásticos de Coca-Cola en océanos llegarán a 600.000 toneladas en 2030, según estudio",
                "imagen": "mundial-1.jpg",
                "texto": """
                Un reciente informe de la organización sin fines de lucro Oceana proyecta que, para el año 2030, los productos de Coca-Cola podrían generar más de 600.000 toneladas de residuos plásticos vertidos anualmente en los océanos y vías fluviales del mundo. Esta cifra alarmante equivale a aproximadamente 220.000 millones de botellas de 500 mililitros, lo que representa una amenaza significativa para la vida marina y los ecosistemas acuáticos. El informe llega en un contexto global marcado por la creciente presencia de microplásticos. 
                El estudio destaca que Coca-Cola es actualmente el mayor contaminador de plástico a nivel mundial, seguida por empresas como PepsiCo, Nestlé, Danone y Altria. La previsión se basa en datos de envases publicados por Coca-Cola entre 2018 y 2023, combinados con estimaciones de crecimiento de ventas. Según Oceana, una solución efectiva para reducir esta contaminación sería implementar envases reutilizables. 
                 Habrá 600.000 toneladas de plástico de Coca-Cola para el 2030

                La estimación se basa en un modelo científico publicado en la revista Science en 2024, que calcula la proporción de residuos que llegan a ecosistemas acuáticos. Según el análisis, la cifra equivale a casi 220.000 millones de botellas plásticas de 500 mililitros. 
                La ONG señala que la solución más efectiva pasa por retomar el uso de envases reutilizables, como las botellas de vidrio retornables, que pueden reutilizarse hasta 50 veces, o los envases de plástico PET reforzado, diseñados para al menos 25 usos. Estas alternativas, según los expertos, permitirían reducir drásticamente la contaminación y limitar la dependencia de plásticos de un solo uso.
                "La contaminación de los océanos es enorme"
                El informe se publica en un contexto de creciente preocupación por el impacto de los microplásticos en la salud humana, vinculados a enfermedades como el cáncer, problemas cardiovasculares e infertilidad. "Coca-Cola es, de lejos, el mayor fabricante y vendedor de bebidas del mundo. Por eso, su responsabilidad en la contaminación de los océanos es enorme", afirmó Matt Littlejohn, vicepresidente de campañas de Oceana, quien instó a la compañía a asumir un rol más activo en la solución del problema. 
                """
            },

            {
                "id": 2,
                "titulo": " La contaminación causó 9 millones de muertes en 2019",
                "imagen": "mundial-2.jpg",
                "texto": """
                Las repercusiones de la contaminación ambiental en nuestra salud siguen siendo muchas y preocupantes, y más aún en los llamados "países en vías de desarrollo". La contaminación, normalmente en las ciudades, provocó en 2019 nueve millones de muertes en todo el mundo, cifra que prácticamente no ha variado desde que se realizó el último estudio sobre el tema, en 2015. Así, en la actualización del informe The Lancet Commission on Pollution and Health, publicado en The Lancet Planetary Health, su autor principal, Richard Fuller, ha destacado que "pese a las graves consecuencias sanitarias, sociales y económicas, la prevención de la contaminación se pasa por alto, en gran medida, en la agenda internacional de desarrollo". El estudio afirma asimismo que, a pesar de que el número de muertes por fuentes de contaminación asociadas a la pobreza extrema, como la mala calidad del aire en interiores o la contaminación del agua, haya disminuido, estas reducciones desafortunadamente se ven contrarrestadas por un aumento de los fallecimientos como consecuencia de la contaminación industrial y química del aire que respiramos.
                De hecho, en 2019, de los nueve millones de muertes en todo el planeta atribuibles a la contaminación, la mala calidad del aire, tanto doméstica como ambiental, fue la responsable de 6,67 millones; la contaminación del agua, de 1,36 millones; el plomo provocó 900.000 muertes, y los riesgos laborales tóxicos causaron 870.000 muertes. A este respecto, Philip Landrigan, director del Programa de Salud Pública Global y del Observatorio de la Contaminación Global del Boston College y uno de los autores del informe, afirma que "la contaminación sigue siendo la mayor amenaza existencial para la salud humana y planetaria y pone en peligro la sostenibilidad de las sociedades modernas. La prevención de la contaminación también puede ralentizar el cambio climático –logrando un doble beneficio para la salud planetaria– y nuestro informe pide una transición masiva y rápida para abandonar todos los combustibles fósiles y pasar a las energías limpias y renovables".
                La contaminación, una arma silenciosa
                En cuanto al descenso de las muertes causadas por la contaminación del aire en los hogares y por el consumo de agua no potable desde el año 2000 es más evidente en África. Esto se debe a las mejoras en el suministro hidráulico, en el saneamiento, a la presencia de combustibles más limpios y a una mayor facilidad de acceso a antibióticos y tratamientos médicos. Sin embargo, como hemos apuntado, este descenso de la mortalidad se ha visto contrarrestado por un aumento importante de las muertes por exposición a la contaminación por plomo y otras formas de contaminación química en todo el mundo durante los últimos veinte años, en especial en el Sudeste Asiático, donde al aumento de los niveles de contaminación industrial se ha de añadir el envejecimiento de la población y un incremento del número de personas expuestas a esta amenaza.
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