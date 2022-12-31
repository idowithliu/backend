# syntax=docker/dockerfile:1
FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN python3 -m pip install -r requirements.txt
#CMD ["gunicorn", "core.wsgi", "-b", "0.0.0.0:8000"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
