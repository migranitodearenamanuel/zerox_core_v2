# nucleo/sentidos.py
# 🗣️ LA VOZ DEL ROBOT (SISTEMA DISCORD)
# Este archivo sirve para que el robot nos mande mensajes al móvil.
# Usamos Discord porque es gratis y rápido.

import os  # Herramientas para mirar dentro del ordenador.
import requests  # El cartero que lleva las cartas por internet.
from dotenv import load_dotenv  # La herramienta para leer las claves secretas.

# Cargamos el archivo .env para poder leer la dirección de Discord.
load_dotenv()

class Comunicador:
    def __init__(self):
        """
        Al encender el comunicador, buscamos la dirección del buzón.
        """
        # Buscamos la variable DISCORD_WEBHOOK_URL en el archivo secreto.
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    def enviar_alerta(self, mensaje: str):
        """
        Envía un mensaje de texto a nuestro canal de Discord.
        Si internet falla, el robot NO se para, solo avisa del error.
        """
        # Si no encontramos la dirección en el archivo .env...
        if not self.webhook_url:
            print("⚠️ AVISO: No puedo hablar. Falta DISCORD_WEBHOOK_URL en el archivo .env")
            return  # ...no hacemos nada más.

        # Preparamos el paquete de datos (JSON) que Discord entiende.
        datos = {
            "content": mensaje  # Aquí va el texto que queremos enviar.
        }

        try:
            # Le damos la carta al cartero (POST) para que la lleve a Discord.
            respuesta = requests.post(self.webhook_url, json=datos)
            
            # Si Discord responde con un código 2xx, todo fue bien.
            if respuesta.status_code >= 200 and respuesta.status_code < 300:
                print("✅ Mensaje entregado a Discord.")
            else:
                print(f"⚠️ Discord recibió el mensaje pero se quejó: {respuesta.status_code}")

        except Exception as e:
            # Si se corta el cable de internet o pasa algo malo...
            print(f"❌ Error enviando mensaje (pero sigo trabajando): {e}")
