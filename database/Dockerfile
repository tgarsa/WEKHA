FROM postgres:16.2-bullseye

LABEL authors="TGARSA"
LABEL description="PostgreSQL Image for demo"
LABEL version="1.0"

# to add the initialization scripts
COPY *.sql /docker-entrypoint-initdb.d/