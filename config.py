# config.py
# ARCHIVO DE CONFIGURACIÓN MAESTRO (VERSIÓN CLOUD LIGERA)
# Solo lo esencial. Sin grasa.

import os
from dotenv import load_dotenv

# Cargamos las variables del archivo .env si existe
load_dotenv()

# --- 1. CREDENCIALES DE INTELIGENCIA (LOS CEREBROS) ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# --- 2. CREDENCIALES DE EXCHANGE (LA BILLETERA) ---
# Usamos Bitget como ejemplo, pero CCXT soporta muchos más
EXCHANGE_ID = "bitget"
API_KEY = os.getenv("BITGET_API_KEY", "")
API_SECRET = os.getenv("BITGET_SECRET", "")
API_PASS = os.getenv("BITGET_PASSWORD", "")

# --- 3. AUTO-EVOLUCIÓN (EL ADN) ---
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
USERNAME_GIT = "ZEROX-BOT"
EMAIL_GIT = "bot@zerox.ai"  # Para firmar los commits
REPO_URL = "https://github.com/TU_USUARIO/TU_REPO.git"  # Cambiar por el real

# --- 4. REDES BARATAS (AUTOPISTAS) ---
# Endpoints RPC para consultar la blockchain directamente si hace falta
RPC_SOLANA = "https://api.mainnet-beta.solana.com"
RPC_BASE = "https://mainnet.base.org"

# --- 5. PARÁMETROS DE TRADING (REGLAS DE JUEGO) ---
SYMBOL = "SOL/USDT"  # Operamos Solana porque es rápido y barato
TIMEFRAME = "15m"    # Velas de 15 minutos
MONTO_APUESTA = 15.0 # Jugamos con 15 USD (o lo que permita la cuenta)
LEVERAGE = 5         # Apalancamiento x5 (Cuidado aquí)
