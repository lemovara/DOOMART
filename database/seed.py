from db import get_db, init_db


def insertar_datos():

    init_db()

    db = get_db()

    try:

        # ==================================================
        # LIMPIAR PRODUCTOS Y EMPRESAS
        # ==================================================

        db.execute("DELETE FROM productos")
        db.execute("DELETE FROM empresas")


        # ==================================================
        # EMPRESAS
        # ==================================================

        empresas = [

            (
                "COCA COLA CO",
                "Empresa de bebidas.",
                "Empresa de bebidas.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de verificación."
            ),

            (
                "PEPSI CO",
                "Empresa de bebidas.",
                "Empresa de bebidas.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de verificación."
            ),

            (
                "DANONE",
                "Empresa de productos alimenticios.",
                "Productos alimenticios.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de verificación."
            ),

            (
                "CHEVRON",
                "Empresa energética.",
                "Empresa energética.",
                "Pendiente de documentar.",
                "Producción de gases tóxicos.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de verificación."
            ),

            (
                "CHINA COAL",
                "Empresa relacionada con producción energética.",
                "Producción energética.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de verificación."
            ),

            (
                "ARCH COAL",
                "Empresa relacionada con producción energética.",
                "Producción energética.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de documentar.",
                "Pendiente de verificación."
            )

        ]


        db.executemany(
            """
            INSERT INTO empresas
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


        # ==================================================
        # OBTENER IDS DE LAS EMPRESAS
        # ==================================================

        registros = db.execute(
            """
            SELECT id, nombre
            FROM empresas
            """
        ).fetchall()


        empresa_ids = {
            empresa["nombre"]: empresa["id"]
            for empresa in registros
        }


        # ==================================================
        # PRODUCTOS
        # ==================================================

        productos = [

            (
                "Coca-Cola",
                "Producto de consumo masivo.",
                "Producto asociado a COCA COLA CO.",
                "coca-cola.png",
                "DIABETES",
                "mas_daninos",
                empresa_ids["COCA COLA CO"]
            ),

            (
                "Pepsi",
                "Producto de consumo masivo.",
                "Producto asociado a PEPSI CO.",
                "pepsi.png",
                "OBESIDAD",
                "mas_daninos",
                empresa_ids["PEPSI CO"]
            ),

            (
                "Danone",
                "Producto alimenticio.",
                "Producto asociado a DANONE.",
                "danone.png",
                "DIABETES",
                "mas_daninos",
                empresa_ids["DANONE"]
            ),

            (
                "Chevron",
                "Empresa relacionada con energía.",
                "Producto asociado a CHEVRON.",
                "chevron.png",
                "CONTAMINACIÓN",
                "pulmones",
                empresa_ids["CHEVRON"]
            ),

            (
                "China Coal",
                "Producción energética.",
                "Producto asociado a CHINA COAL.",
                "china-coal.png",
                "CALIDAD DEL AIRE",
                "pulmones",
                empresa_ids["CHINA COAL"]
            ),

            (
                "ARCH Coal",
                "Producción energética.",
                "Producto asociado a ARCH COAL.",
                "arch-coal.png",
                "GASES TÓXICOS",
                "pulmones",
                empresa_ids["ARCH COAL"]
            )

        ]


        # ==================================================
        # INSERTAR PRODUCTOS
        # ==================================================

        db.executemany(
            """
            INSERT INTO productos
            (
                nombre,
                leyenda,
                descripcion,
                imagen,
                etiqueta,
                seccion,
                empresa_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            productos
        )


        # ==================================================
        # GUARDAR CAMBIOS
        # ==================================================

        db.commit()

        print("DOOMART: base de datos cargada correctamente.")


    finally:

        db.close()


if __name__ == "__main__":
    insertar_datos()