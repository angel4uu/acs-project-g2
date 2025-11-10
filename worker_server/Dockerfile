FROM python:3.11-slim

# Añade esta línea para forzar a Python a imprimir logs inmediatamente
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the worker application files
COPY ./app /app/app

# The CMD starts the worker script, not a web server
CMD ["python", "-m", "app.worker"]