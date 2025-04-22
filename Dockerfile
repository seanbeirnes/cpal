FROM node:23 AS frontend-builder

WORKDIR /app/frontend

COPY frontend/ .

RUN npm install
RUN npm run build

FROM python:3.13-slim AS backend-builder

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY --from=backend-builder /opt/venv /opt/venv

WORKDIR /app
COPY --from=frontend-builder /app/frontend/dist ./static
COPY backend/ .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1\
    PATH="/opt/venv/bin:$PATH"

EXPOSE 8080/tcp

CMD ["fastapi", "run", "main.py", "--port", "8080"]

