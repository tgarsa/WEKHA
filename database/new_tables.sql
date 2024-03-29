
-- CREATE TABLES Campeonatos

DROP TABLE IF EXISTS campeonatos;
CREATE TABLE campeonatos (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       nombre VARCHAR NOT NULL,
       lugar VARCHAR NOT NULL,
       id_sede VARCHAR NOT NULL,
       id_organizador VARCHAR NOT NULL,
       fecha TIMESTAMP NOT NULL,
       jugadores INTEGER NOT NULL,
       turnos INTEGER NOT NULL,
       jugadores_mesa INTEGER NOT NULL,
       filas INTEGER NOT NULL,
       columnas INTEGER NOT NULL,
       rondas INTEGER NOT NULL
);

DROP TABLE IF EXISTS campeonatos_arbitros;
CREATE TABLE campeonatos_arbitros (
       id_table SERIAL PRIMARY KEY,
       id_campeonato VARCHAR NOT NULL,
       id_arbitro VARCHAR NOT NULL
);


DROP TABLE IF EXISTS campeonatos_jugadores;
CREATE TABLE campeonatos_jugadores (
       id_table SERIAL PRIMARY KEY,
       id_campeonato VARCHAR NOT NULL,
       id_jugadores VARCHAR NOT NULL
);


DROP TABLE IF EXISTS campeonatos_jugadas;
CREATE TABLE campeonatos_jugadas (
       id_table SERIAL PRIMARY KEY,
       id_campeonato VARCHAR NOT NULL,
       id_prueba VARCHAR NOT NULL,
       id_mesa VARCHAR NOT NULL,
       id_ronda VARCHAR NOT NULL,
       id_arbitro VARCHAR NOT NULL,
       acc_penals INTEGER NOT NULL,
       acc_desem INTEGER NOT NULL -- Acumulado puntos desempates.
);


-- CREATE TABLES Pruebas

DROP TABLE IF EXISTS pruebas;
CREATE TABLE pruebas (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       nombre VARCHAR NOT NULL,
       enunciado VARCHAR NOT NULL,
       material VARCHAR NOT NULL,
       discapacidades VARCHAR NOT NULL,
       observaciones VARCHAR NOT NULL
);


-- CREATE TABLES Jugadores

DROP TABLE IF EXISTS jugadores_bronze;
CREATE TABLE jugadores_bronze (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       dni VARCHAR,
       nombre VARCHAR,
       apellidos VARCHAR,
       nick VARCHAR,
       email VARCHAR,
       telefono VARCHAR,
       residencia VARCHAR,
       pais VARCHAR,
       talla VARCHAR,
       discapacidades VARCHAR,
       observaciones VARCHAR,
       created_at TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS jugadores;
CREATE TABLE jugadores (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       dni VARCHAR NOT NULL,
       nombre VARCHAR NOT NULL,
       apellidos VARCHAR NOT NULL,
       nick VARCHAR NOT NULL,
       email VARCHAR NOT NULL,
       telefono VARCHAR NOT NULL,
       residencia VARCHAR NOT NULL,
       pais VARCHAR NOT NULL,
       talla VARCHAR NOT NULL,
       discapacidades VARCHAR NOT NULL,
       observaciones VARCHAR,
       created_at TIMESTAMP NOT NULL,
       updated_at TIMESTAMP NOT NULL
);


DROP TABLE IF EXISTS jugadores_campeonato;
CREATE TABLE jugadores_campeonato (
       id_table SERIAL PRIMARY KEY,
       id_jugador VARCHAR NOT NULL,
       id_campeonato VARCHAR NOT NULL,
       acc_penal INTEGER NOT NULL,
       acc_desem INTEGER NOT NULL, -- Acumulado puntos desempates.
       puesto INTEGER NOT NULL
);

DROP TABLE IF EXISTS jugadores_pruebas;
CREATE TABLE jugadores_pruebas (
       id_table SERIAL PRIMARY KEY,
       id_jugador VARCHAR NOT NULL,
       id_campeonato VARCHAR NOT NULL,
       id_prueba VARCHAR NOT NULL,
       ronda INTEGER NOT NULL,
       propuesta VARCHAR NOT NULL,
       resultado VARCHAR NOT NULL,
       penal INTEGER NOT NULL,
       desem INTEGER NOT NULL -- Puntos desempates.
);

-- CREATE TABLES Sedes

DROP TABLE IF EXISTS sedes;
CREATE TABLE sedes (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       edificio VARCHAR,
       provincia VARCHAR NOT NULL,
       localidad VARCHAR NOT NULL,
       postal VARCHAR NOT NULL,
       calle VARCHAR NOT NULL,
       numero INTEGER NOT NULL,
       anadido VARCHAR,
       accesible BOOLEAN NOT NULL,
       tamano INTEGER NOT NULL,
       observaciones VARCHAR,
       dep_cont VARCHAR,
       per_cont VARCHAR,
       tel_cont VARCHAR,
       email_cont VARCHAR,
       created_at TIMESTAMP NOT NULL,
       updated_at TIMESTAMP NOT NULL
);

-- CREATE TABLES Licencias

DROP TABLE IF EXISTS licencias;
CREATE TABLE licencias (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       id_jugador VARCHAR NOT NULL,
       hasta TIMESTAMP,
       ambito VARCHAR NOT NULL,
       created_at TIMESTAMP NOT NULL,
       updated_at TIMESTAMP NOT NULL
);

-- CREATE TABLES Patrocinadores

DROP TABLE IF EXISTS patrocinadores;
CREATE TABLE patrocinadores (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       nombre VARCHAR NOT NULL,
       actividad VARCHAR NOT NULL,
       dep_cont VARCHAR,
       per_cont VARCHAR,
       tel_cont VARCHAR,
       email_cont VARCHAR,
       observaciones VARCHAR,
       created_at TIMESTAMP NOT NULL,
       updated_at TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS patrocinios;
CREATE TABLE patrocinios (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       id_patrocinador VARCHAR NOT NULL,
       id_campeonato VARCHAR NOT NULL,
       aportacion VARCHAR NOT NULL,
       observaciones VARCHAR,
       created_at TIMESTAMP NOT NULL,
       updated_at TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS alojamientos;
CREATE TABLE alojamientos (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       nombre VARCHAR NOT NULL,
       edificio VARCHAR,
       provincia VARCHAR NOT NULL,
       localidad VARCHAR NOT NULL,
       postal VARCHAR NOT NULL,
       calle VARCHAR NOT NULL,
       numero INTEGER NOT NULL,
       anadido VARCHAR,
       accesible BOOLEAN NOT NULL,
       dep_cont VARCHAR,
       per_cont VARCHAR,
       tel_cont VARCHAR,
       email_cont VARCHAR,
       observaciones VARCHAR,
       created_at TIMESTAMP NOT NULL,
       updated_at TIMESTAMP NOT NULL
);