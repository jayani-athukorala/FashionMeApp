# Use the official PostgreSQL image as the base image
FROM postgres:13

# Set environment variables
ENV POSTGRES_USER="root"
ENV POSTGRES_PASSWORD="root"
ENV POSTGRES_DB="fashionme_db"

# Copy SQL scripts to initialize the database
COPY 01_schema.sql /docker-entrypoint-initdb.d/
COPY 02_data.sql /docker-entrypoint-initdb.d/

# Copy initial images to a directory within the container
COPY images /docker-entrypoint-initdb.d/initial-images


