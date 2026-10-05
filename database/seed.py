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
        "Empresa multinacional de bebidas y productos de consumo.",
        "Produce y comercializa bebidas, utilizando agua, envases de plástico, aluminio y otros materiales. Sus principales aspectos ambientales incluyen consumo de agua, empaques y emisiones asociadas a sus operaciones y cadena de suministro.",
        "La producción de ingredientes agrícolas y la extracción de materias primas para los envases pueden generar impactos sobre el suelo. La empresa trabaja con proveedores agrícolas para mejorar prácticas de abastecimiento.",
        "Las operaciones y la cadena de suministro generan emisiones de gases de efecto invernadero. Coca-Cola señala como áreas de trabajo la reducción de emisiones y el uso de electricidad renovable.",
        "El agua es un recurso fundamental para la fabricación de sus bebidas. La empresa establece objetivos de reposición de agua y de eficiencia hídrica, especialmente en zonas de alto riesgo hídrico.",
        "Utiliza grandes cantidades de agua, energía, materias primas agrícolas y materiales para fabricar y distribuir sus productos.",
        "Sus productos utilizan principalmente envases de plástico, aluminio y vidrio. La empresa trabaja en aumentar el contenido reciclado y mejorar la recolección y reciclaje de botellas y latas.",
        "Coca-Cola Company, Environmental Policy y Environment, información ambiental consultada en Septiembre 2026."
    ),

    (
        "PEPSI CO",
        "Empresa multinacional de alimentos y bebidas.",
        "Produce bebidas y alimentos de consumo masivo. Sus impactos ambientales están relacionados principalmente con agricultura, energía, agua, emisiones y materiales de empaque.",
        "La producción agrícola de ingredientes puede afectar el suelo mediante el uso de agua, fertilizantes y prácticas agrícolas. PepsiCo desarrolla programas de agricultura regenerativa, restaurativa y protectora.",
        "La fabricación, transporte, agricultura y cadena de suministro generan emisiones de gases de efecto invernadero. PepsiCo reporta objetivos de reducción de emisiones y transición energética.",
        "La fabricación de bebidas y alimentos requiere agua. PepsiCo tiene programas de eficiencia y reposición de agua, especialmente en instalaciones ubicadas en zonas de alto riesgo hídrico.",
        "Utiliza agua, energía, productos agrícolas, combustibles y materias primas para fabricar, transportar y distribuir sus productos.",
        "Utiliza cantidades importantes de plástico para sus envases. En 2025 reportó una reducción del 6% en el tonelaje absoluto de plástico virgen de ciertos envases primarios y un 18% de plástico reciclado en esos mercados.",
        "PepsiCo, 2025 ESG Summary, Water, Packaging y Agriculture."
    ),

    (
        "DANONE",
        "Empresa multinacional de productos alimenticios y bebidas.",
        "Produce productos lácteos, bebidas, alimentos especializados y agua embotellada. Sus principales impactos ambientales están relacionados con agricultura, producción láctea, agua, emisiones y empaques.",
        "La producción de leche y otros ingredientes agrícolas puede afectar el suelo. Danone trabaja con productores en prácticas relacionadas con manejo del estiércol, salud del suelo y gestión de nutrientes.",
        "La producción láctea genera emisiones de gases de efecto invernadero, especialmente metano asociado a la ganadería. Danone reportó una reducción del 29.8% de las emisiones de metano de su suministro de leche fresca respecto a 2020.",
        "El agua es utilizada en la producción de alimentos, bebidas y agua embotellada. La empresa trabaja en proyectos relacionados con eficiencia, tratamiento de aguas y protección de recursos hídricos.",
        "Utiliza leche, ingredientes agrícolas, agua, energía y materiales de empaque para fabricar y distribuir sus productos.",
        "Los productos utilizan plástico, vidrio, papel y otros materiales. Danone reporta acciones para reducir plástico virgen, aumentar material reciclado y mejorar la reciclabilidad de sus envases.",
        "Danone, Integrated Annual Report 2025 y Sustainability / Nature reports."
    ),

    (
        "CHEVRON",
        "Empresa energética dedicada principalmente a la producción y comercialización de petróleo, gas natural y productos derivados.",
        "Sus actividades incluyen producción de petróleo y gas, refinación, combustibles, lubricantes, petroquímicos y otros productos energéticos.",
        "La extracción de petróleo y gas puede alterar el terreno y requiere infraestructura, caminos, pozos y otras instalaciones. Las operaciones también pueden generar impactos derivados de derrames o actividades de extracción.",
        "La producción y procesamiento de combustibles fósiles generan emisiones de gases de efecto invernadero y otros contaminantes atmosféricos. Chevron reporta acciones y métricas relacionadas con emisiones y reducción de intensidad de carbono.",
        "Las operaciones petroleras y de refinación utilizan agua. Chevron reporta extracción y consumo de agua dulce, incluyendo operaciones ubicadas en regiones con estrés hídrico, además de descargas de efluentes.",
        "Utiliza grandes cantidades de petróleo, gas natural, agua, energía, materiales industriales y combustibles durante las etapas de extracción, procesamiento y distribución.",
        "Las operaciones generan residuos industriales y materiales derivados de la extracción y procesamiento de hidrocarburos. También existen riesgos asociados a derrames de petróleo sobre suelo y agua.",
        "Chevron, 2024 Corporate Sustainability Highlights y Corporate Sustainability Reporting."
    ),

    (
        "CHINA COAL",
        "Empresa china dedicada principalmente a la producción y comercialización de carbón y actividades energéticas relacionadas.",
        "Sus actividades incluyen minería de carbón, producción energética y otras operaciones relacionadas con la cadena de suministro del carbón.",
        "La minería de carbón modifica el terreno y puede requerir actividades de restauración y rehabilitación. La extracción también genera residuos mineros como ganga de carbón.",
        "Las actividades relacionadas con el carbón generan emisiones de gases de efecto invernadero y contaminantes atmosféricos. En 2025 China Coal Energy reportó emisiones de dióxido de azufre, óxidos de nitrógeno, humo y compuestos orgánicos volátiles.",
        "La minería utiliza agua y puede generar aguas residuales. China Coal Energy reporta reutilización de agua de mina y una tasa de reutilización de agua del 98.3% en 2025.",
        "La actividad requiere grandes cantidades de carbón, energía, electricidad, combustibles y agua. La empresa también utiliza infraestructura y materiales para extracción, procesamiento y transporte.",
        "La minería genera ganga de carbón, residuos industriales y otros residuos. La empresa reporta iniciativas de aprovechamiento de ganga y economía circular, además de materiales de embalaje utilizados en sus operaciones.",
        "China Coal Energy, 2025 Environmental, Social and Governance Report."
    ),

    (
        "ARCH COAL",
        "Empresa relacionada con la producción de carbón y actividades de minería energética.",
        "Sus operaciones están relacionadas con la extracción, procesamiento y comercialización de carbón. Sus principales aspectos ambientales incluyen emisiones, uso de agua, residuos mineros y recuperación de terrenos.",
        "La minería de carbón puede modificar el terreno y requiere procesos de recuperación y restauración de las áreas intervenidas. Las operaciones también generan residuos derivados de la extracción y procesamiento del carbón.",
        "La extracción y procesamiento del carbón generan emisiones de gases de efecto invernadero y otros contaminantes. La empresa reporta acciones destinadas a reducir sus impactos ambientales.",
        "Las operaciones mineras requieren agua, incluyendo procesos de preparación y lavado del carbón. Arch ha reportado reutilización y reciclaje de agua dentro de sus operaciones para reducir la extracción de nuevas fuentes.",
        "Utiliza grandes cantidades de carbón, energía, combustibles, agua y materiales necesarios para las actividades de extracción, procesamiento y transporte.",
        "Las operaciones generan residuos mineros y materiales asociados al procesamiento del carbón. Arch ha reportado programas de reciclaje, reutilización de agua y recuperación de áreas mineras.",
        "Arch Resources, Sustainability Report 2022."
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