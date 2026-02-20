# nucleo/conector_exchange.py
# AQUÍ ESTÁ EL TELÉFONO PARA LLAMAR A LA TIENDA (BITGET)
# Este archivo se encarga de hablar con el mercado.

import ccxt  # Me traigo el libro de idiomas para hablar con todas las tiendas
import time  # Me traigo el reloj
import sys
import os

# Truco para encontrar la configuración
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config  # Me traigo las llaves de la tienda


class ConectorBitget:  # El Telefonista
    def __init__(self):  # Cuando empieza a trabajar
        self.conexion = None  # Todavía no ha llamado
        self.conectar()  # Llama a la tienda ahora mismo

    def conectar(self):  # Marcar el número
        try:
            # Configuro el teléfono con las claves secretas
            self.conexion = ccxt.bitget(
                {
                    "apiKey": config.API_KEY,
                    "secret": config.API_SECRET,
                    "password": config.API_PASS,
                    "options": {
                        "defaultType": "swap"
                    },  # Le digo que quiero jugar a futuros
                }
            )
            print("📞 TELÉFONO: Conectado con Bitget Correctamente.")
        except Exception as e:
            print(f"📞 TELÉFONO: ¡Error! No pude llamar. {e}")
            self.conexion = None

    def obtener_saldo(self):  # Preguntar cuánto dinero tengo en la hucha
        if not self.conexion:
            return 0.0  # Si no hay línea, tengo cero
        try:
            balance = self.conexion.fetch_balance()  # Pido el extracto bancario
            # Busco los USDT que tengo libres
            dinero = balance["USDT"]["total"]
            return float(dinero)  # Digo cuánto hay
        except Exception as e:
            print(f"📞 TELÉFONO: No me dicen el saldo. {e}")
            return 0.0

    def obtener_precio(self, simbolo):  # Preguntar cuánto vale algo
        if not self.conexion:
            return 0.0
        try:
            ticker = self.conexion.fetch_ticker(simbolo)  # Miro el precio en el cartel
            return float(ticker["last"])  # Devuelvo el último precio
        except Exception as e:
            print(f"📞 TELÉFONO: No veo el precio de {simbolo}. {e}")
            return 0.0
