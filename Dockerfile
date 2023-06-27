FROM python:3.8-slim@sha256:10e07e36f86af4371accc42642852aa60eab74e6896fc065345ebc2c576eec0d

LABEL org.opencontainers.image.authors="Jimmy Liu <contact@jimmyliu.dev>"
LABEL org.opencontainers.image.source="https://github.com/idowithliu/backend"

# Copy files
WORKDIR /app
COPY . /app
COPY ./core/docker-settings.py /app/core/config.py
COPY ./core/config.py /app/core/docker-config.py

# Install dependencies
RUN apt-get update && \
    apt-get install -y build-essential python3-dev libpq-dev libffi-dev libssl-dev
RUN python3 -m pip install -r requirements.txt
# RUN python3 manage.py migrate

# Start worker
CMD ["python3", "gunicorn", "core.wsgi", "-b", "0.0.0.0:8000"]
EXPOSE 8000
