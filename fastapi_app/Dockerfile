FROM python:3.13.13-alpine

ENV PATH="${PATH}:/root/.local/bin"
COPY ./src /app/src
COPY ./src/alembic /app/alembic
COPY ./src/alembic.ini /app/alembic.ini
COPY requirements.txt /app/
COPY ./images /images

ENV PYTHONPATH /app/src
COPY .env /app/.env
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN chmod +x /app/src/start.sh
EXPOSE 8000