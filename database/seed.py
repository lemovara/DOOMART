# =========================================================
# DOOMART
# Datos iniciales para SQLite
# =========================================================

from db import get_db, init_db


def insertar_datos():

    # Primero comprobamos que las tablas existan.
    init_db()

    db = get_db()

    try:

        # =================================================
        # EMPRESAS
        # =================================================

        empresas = [

            (
                "COCA COLA CO",
                "Empresa utilizada como ejemplo dentro del proyecto DOOMART.",
                "Empresa de bebidas.",
                "Dato de ejemplo indicado en el documento del proyecto.",
                "No especificado en el documento.",
                "No especificado en el documento.",
                "55 mil millones de litros de agua consumidos.",
                "No especificado en el documento.",
                "Dato de ejemplo del documento; verificar y documentar "
                "la fuente antes de usarlo como dato público."
            ),

            (
                "PEPSI CO",
                "Empresa utilizada como ejemplo dentro del proyecto DOOMART.",
                "Empresa de bebidas.",
                "No especificado en el documento.",
                "No especificado en el documento.",
                "No especificado en el documento.",
                "No especificado en el documento.",
                "No especificado en el documento.",
                "Ejemplo tomado del documento del proyecto."
            ),

            (
                "CHEVRON",
                "Empresa utilizada como ejemplo dentro del proyecto DOOMART.",
                "Empresa relacionada con producción energética.",
                "No especificado en el documento.",
                "Producción de gases tóxicos.",
                "No especificado en el documento.",
                "No especificado en el documento.",
                "No especificado en el documento.",
                "Dato de ejemplo del documento; verificar y documentar "
                "la fuente antes de usarlo como dato público."
            )

        ]


        # -------------------------------------------------
        # INSERTAR EMPRESAS
        # -------------------------------------------------

        db.executemany(
            """
            INSERT OR IGNORE INTO empresas
            (
                nombre,
                descripcion,
                caracteristicas,
                danio_suelo,
                danio_aire,
                danio_agua,
                uso_recursos,
                plasticos_residuos,
                fuente
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            empresas
        )


        # =================================================
        # OBTENER IDS DE LAS EMPRESAS
        # =================================================

        empresas_db = db.execute(
            """
            SELECT id, nombre
            FROM empresas
            """
        ).fetchall()

        empresa_ids = {
            empresa["nombre"]: empresa["id"]
            for empresa in empresas_db
        }


        # =================================================
        # PRODUCTOS
        # =================================================

        productos = [

            (
                "Coca-Cola",
                "Ejemplo de producto para DOOMART",
                "Producto de demostración asociado a COCA COLA CO.",
                "coca-cola.png",
                empresa_ids["COCA COLA CO"]
            ),

            (
                "Pepsi",
                "Ejemplo de producto para DOOMART",
                "Producto de demostración asociado a PEPSI CO.",
                "pepsi.png",
                empresa_ids["PEPSI CO"]
            ),

            (
                "Chevron",
                "Ejemplo de producto para DOOMART",
                "Producto de demostración asociado a CHEVRON.",
                "chevron.png",
                empresa_ids["CHEVRON"]
            )

        ]


        # -------------------------------------------------
        # INSERTAR PRODUCTOS
        # -------------------------------------------------

        db.executemany(
            """
            INSERT INTO productos
            (
                nombre,
                leyenda,
                descripcion,
                imagen,
                empresa_id
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            productos
        )


        # Guardamos.
        db.commit()

        print("========================================")
        print(" BASE DE DATOS DOOMART INICIALIZADA")
        print("========================================")
        print("Empresas y productos insertados.")
        print("========================================")


    finally:

        db.close()


# ---------------------------------------------------------
# PUNTO DE ENTRADA
# ---------------------------------------------------------

if __name__ == "__main__":
    insertar_datos()