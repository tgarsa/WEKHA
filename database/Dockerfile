FROM postgres:16.2-bullseye

LABEL authors="TGARSA"
LABEL description="PostgreSQL Image for demo"
LABEL version="0.1"

# to add the initialization scripts
COPY *.sql /docker-entrypoint-initdb.d/
