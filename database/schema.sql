CREATE TABLE IF NOT EXISTS empresas (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre TEXT NOT NULL UNIQUE,

    descripcion TEXT,

    caracteristicas TEXT,

    danio_suelo TEXT,

    danio_aire TEXT,

    danio_agua TEXT,

    uso_recursos TEXT,

    plasticos_residuos TEXT,

    fuente TEXT
);


CREATE TABLE IF NOT EXISTS productos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre TEXT NOT NULL,

    leyenda TEXT,

    descripcion TEXT,

    imagen TEXT,

    etiqueta TEXT,

    seccion TEXT NOT NULL,

    empresa_id INTEGER NOT NULL,

    FOREIGN KEY (empresa_id)
        REFERENCES empresas(id)

);