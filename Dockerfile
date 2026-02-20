# Usamos una imagen base ligera y segura de Python 3.11 (Estándar Freqtrade/OpenClaw)
FROM python:3.11-slim-bookworm

# Evitamos que Python genere archivos .pyc y forzamos logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# 1. INSTALACIÓN DE DEPENDENCIAS DEL SISTEMA (Cuerpo Físico)
# He juntado todo en una línea para que Docker no se líe.
# Instalamos las herramientas para construir (build-essential), descargar (wget, curl) y clonar (git).
RUN apt-get update && apt-get install -y build-essential wget git curl && rm -rf /var/lib/apt/lists/*

# 2. INSTALACIÓN DE TA-LIB (El Cerebro Matemático)
# Esto es crítico para las estrategias de Volman y patrones de velas
# Descargamos el código fuente, lo descomprimimos, lo compilamos e instalamos
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# 3. INSTALACIÓN DE LIBRERÍAS PYTHON (Habilidades)
# Copiamos primero los requisitos para aprovechar la caché de Docker
COPY requisitos.txt .
# Actualizamos pip e instalamos las dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requisitos.txt && \
    pip install ta-lib

# 4. INSTALACIÓN DEL CÓDIGO (Alma)
# Copiamos todo el código del proyecto dentro del contenedor
COPY . .

# Permisos de ejecución para el script de entrada
RUN chmod +x entrypoint.sh

# El comando que mantiene vivo al bot
ENTRYPOINT ["./entrypoint.sh"]
