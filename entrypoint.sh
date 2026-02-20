#!/bin/bash
set -e

echo "🚀 INICIANDO PROTOCOLO ZEROX-CLAW..."

# 1. Autocuración de dependencias
# Si la IA ha añadido una librería nueva a requisitos.txt, la instalamos.
if [ -f "requisitos.txt" ]; then
    echo "📦 Verificando dependencias..."
    pip install -r requisitos.txt
fi

# 2. Arranque del Sistema Autónomo
# Ejecutamos el cerebro principal en modo asíncrono
echo "🧠 Conectando redes neuronales..."
python SISTEMA_AUTONOMO.py
