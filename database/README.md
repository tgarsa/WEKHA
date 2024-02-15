# Base de datos

Pensando en la forma de poner en producción el sistema vamos a utilizar un contenedor Docker que contendra de forma independiente el gestor de base de datos. En nuestro caso en particular y pensando en que la maqueta pueda ser despelegada de forma sencilla vamos a utiliar a PostgreSQL como gestor. 

Como vamos a instalar la maqueta en una Raspberry Pi 3, la cual tiene instalada una imagen de Debian Bullseye de 64 bits, la imagen de PostgreSQL que utilizaremos será la "16.2-bullseye" que es la versión más actual el 15-03-2024. 


