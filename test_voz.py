# test_voz.py
# 🧪 PRUEBA DE LA VOZ DEL ROBOT
# Este archivo comprueba si el robot puede hablar por Discord.
# Lo usamos para asegurarnos de que la conexión a internet funciona.

from nucleo.sentidos import Comunicador  # Traemos la herramienta de comunicación.

# Creamos una "boca" nueva para el robot.
boca = Comunicador()

# Preparamos el mensaje de éxito que queremos enviar.
mensaje_prueba = "🚀 ZEROX CONECTADO A DISCORD - Sistema de notificaciones operativo a coste cero."

# Le decimos a la boca que grite el mensaje.
# Si todo va bien, verás ✅ en la consola.
boca.enviar_alerta(mensaje_prueba)
