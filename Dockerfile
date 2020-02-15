# Base image
FROM ubuntu:18.04

# Work directory settings
RUN mkdir /app
WORKDIR /app

# Installations
RUN apt-get update && apt-get install -y python3-pip python3.7
RUN pip3 install Flask waitress SQLALchemy psycopg2-binary

# Local installations
ADD url_shortner.py /app/
COPY templates /app/templates

# Expose application port
EXPOSE 8080

# Command to run app
CMD ["python3", "url_shortner.py"]
