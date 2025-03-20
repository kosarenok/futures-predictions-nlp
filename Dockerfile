FROM python:3.11-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    make \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p logs

FROM base AS backend
EXPOSE 8000
ENV PYTHONPATH=/app
CMD ["python", "src/main/app.py"]

FROM base AS frontend
EXPOSE 8501
ENV PYTHONPATH=/app
ENV BACKEND_URL=http://backend:8000
CMD ["streamlit", "run", "src/main/interface.py", "--server.port=8501", "--server.address=0.0.0.0"]
