
-- CREATE TABLES Campeonatos

DROP TABLE IF EXISTS campeonatos;
CREATE TABLE campeonatos (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       nombre VARCHAR NOT NULL,
       id_sede VARCHAR NOT NULL,
       id_licencia VARCHAR NOT NULL,
       fecha TIMESTAMP NOT NULL,
       jugadores INTEGER NOT NULL,
       turnos INTEGER NOT NULL,
       jugadores_mesa INTEGER NOT NULL,
       filas INTEGER NOT NULL,
       columnas INTEGER NOT NULL,
       rondas INTEGER NOT NULL,
       observaciones VARCHAR,
       created_at TIMESTAMP NOT NULL,
       updated_at TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS campeonatos_arbitros;
CREATE TABLE campeonatos_arbitros (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       id_campeonato VARCHAR NOT NULL,
       id_arbitro VARCHAR NOT NULL,
       created_at TIMESTAMP NOT NULL,
       updated_at TIMESTAMP NOT NULL
);


DROP TABLE IF EXISTS campeonatos_jugadores;
CREATE TABLE campeonatos_jugadores (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       id_campeonato VARCHAR NOT NULL,
       id_jugador VARCHAR NOT NULL,
       created_at TIMESTAMP NOT NULL,
       updated_at TIMESTAMP NOT NULL
);


DROP TABLE IF EXISTS campeonatos_jugadas;
CREATE TABLE campeonatos_jugadas (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       id_campeonato VARCHAR NOT NULL,
       id_prueba VARCHAR NOT NULL,
       id_mesa VARCHAR NOT NULL,
       id_ronda VARCHAR NOT NULL,
       id_arbitro VARCHAR NOT NULL,
       acc_penals INTEGER NOT NULL, -- Acumulado puntos de penalizacion.
       acc_desem INTEGER NOT NULL, -- Acumulado puntos desempates.
       observaciones VARCHAR,
       created_at TIMESTAMP NOT NULL,
       updated_at TIMESTAMP NOT NULL
);


-- CREATE TABLES Pruebas

DROP TABLE IF EXISTS pruebas;
CREATE TABLE pruebas (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       nombre VARCHAR NOT NULL,
       enunciado VARCHAR NOT NULL,
       material VARCHAR NOT NULL,
       discapacidades INTEGER NOT NULL,
       observaciones VARCHAR,
       created_at TIMESTAMP NOT NULL,
       updated_at TIMESTAMP NOT NULL
);


DROP TABLE IF EXISTS mesas;
CREATE TABLE mesas (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       id_campeonato VARCHAR NOT NULL,
       fila INTEGER NOT NULL,
       columna INTEGER NOT NULL,
       observaciones VARCHAR,
       created_at TIMESTAMP NOT NULL,
       updated_at TIMESTAMP NOT NULL
);


DROP TABLE IF EXISTS rondas;
CREATE TABLE rondas (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       nombre VARCHAR NOT NULL,
       observaciones VARCHAR,
       created_at TIMESTAMP NOT NULL,
       updated_at TIMESTAMP NOT NULL
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
       discapacidades INTEGER,
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
       discapacidades INTEGER NOT NULL,
       observaciones VARCHAR,
       created_at TIMESTAMP NOT NULL,
       updated_at TIMESTAMP NOT NULL
);


DROP TABLE IF EXISTS jugadores_campeonato;
CREATE TABLE jugadores_campeonato (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       id_jugador VARCHAR NOT NULL,
       id_campeonato VARCHAR NOT NULL,
       acc_penal INTEGER NOT NULL,
       acc_desem INTEGER NOT NULL, -- Acumulado puntos desempates.
       puesto INTEGER NOT NULL,
       created_at TIMESTAMP NOT NULL,
       updated_at TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS jugadores_pruebas;
CREATE TABLE jugadores_pruebas (
       id_table SERIAL PRIMARY KEY,
       id VARCHAR NOT NULL,
       id_jugador VARCHAR NOT NULL,
       id_campeonato VARCHAR NOT NULL,
       id_prueba VARCHAR NOT NULL,
       id_ronda VARCHAR NOT NULL,
       propuesta INTEGER NOT NULL,
       resultado INTEGER NOT NULL,
       penal INTEGER NOT NULL,
       desem INTEGER NOT NULL,  -- Puntos desempates.
       created_at TIMESTAMP NOT NULL,
       updated_at TIMESTAMP NOT NULL
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
       id_organizador VARCHAR NOT NULL,
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

-- Load the data into the Rondas table.

INSERT into rondas (id, nombre, created_at, updated_at)
VALUES ('RF001', 'Final', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('RF002', 'Semifinal', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('RF003', 'Cuartos de final', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('RF004', 'Octavos de final', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('R010', 'Decima Ronda', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('R009', 'Novena Ronda', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('R008', 'Octaba Ronda', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('R007', 'Septima Ronda', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('R006', 'Sexta Ronda', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('R005', 'Quinta Ronda', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('R004', 'Cuarta Ronda', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('R003', 'Tercera Ronda', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('R002', 'Segunda Ronda', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('R001', 'Primera Ronda', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)

