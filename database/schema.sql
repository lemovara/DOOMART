-- =========================================================
-- DOOMART
-- Estructura inicial de la base de datos
-- =========================================================


-- =========================================================
-- TABLA: empresas
-- =========================================================
-- Aquí almacenamos la información ambiental/social
-- asociada con cada empresa.
--
-- Los campos corresponden a los requerimientos del
-- proyecto.
-- =========================================================

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


-- =========================================================
-- TABLA: productos
-- =========================================================
-- Un producto pertenece a una empresa.
--
-- Ejemplo:
--
-- Coca-Cola
--      ↓
-- Coca-Cola (producto)
--
-- Pepsi
--      ↓
-- Producto Pepsi
--
-- etc.
-- =========================================================

CREATE TABLE IF NOT EXISTS productos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre TEXT NOT NULL,

    leyenda TEXT,

    descripcion TEXT,

    imagen TEXT,

    empresa_id INTEGER NOT NULL,

    FOREIGN KEY (empresa_id)
        REFERENCES empresas(id)
);