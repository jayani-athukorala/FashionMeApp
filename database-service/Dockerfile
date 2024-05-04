# Use the official PostgreSQL image as the base image
FROM postgres:13

# Set environment variables
ENV POSTGRES_USER "root"
ENV POSTGRES_PASSWORD "root"
ENV POSTGRES_DB "fashionme_db"

# Copy SQL scripts to initialize the database
# Ensure the schema.sql runs before data.sql by naming accordingly
COPY init.sql /docker-entrypoint-initdb.d/


