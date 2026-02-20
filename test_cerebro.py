# test_cerebro.py
# 🧪 EL BANCO DE PRUEBAS (CON VOZ)
# Este archivo prueba si el cerebro piensa bien Y si nos lo cuenta por Discord.
# Es como un simulacro de operación real.

from nucleo.orquestador_agentes import CEREBRO_ZEROX  # Traemos el cerebro que piensa.
from nucleo.sentidos import Comunicador             # Traemos la boca que habla.

# 1. Preparamos el robot
boca = Comunicador() # Le ponemos la boca para que pueda hablar.

print("🧠 Arrancando ZEROX para una prueba de simulación...")

# 2. Definimos la situación inicial
# Imaginamos que tenemos 15 euros y el diario está vacío.
estado_inicial = {
    "capital": 15.0,
    "historial": ["--- INICIANDO ZEROX (SIMULACIÓN) ---"]
}

# 3. ¡A PENSAR!
# El robot ejecuta todos los pasos (Scout -> Auditor -> Quant -> Reflector).
resultado = CEREBRO_ZEROX.invoke(estado_inicial)

# 4. Preparamos el informe para los humanos
# Creamos un texto bonito con un título en negrita para Discord.
mensaje_discord = "🖥️ **INFORME DE OPERACIÓN ZEROX**\n\n"

# Leemos el diario paso a paso y lo añadimos al mensaje.
if "historial" in resultado:
    for paso in resultado["historial"]:
        print(paso) # Lo mostramos en tu pantalla negra (consola).
        mensaje_discord += f"• {paso}\n" # Lo añadimos a la carta de Discord con un puntito.

# Miramos cuánto dinero ha decidido usar al final.
dinero_arriesgado = resultado.get('tamaño_operacion', 0)

# Preparamos la frase final del dinero.
texto_dinero = f"\n💰 **Capital Final Arriesgado:** {dinero_arriesgado:.2f}€"

print(texto_dinero) # Lo mostramos en tu pantalla.
mensaje_discord += texto_dinero # Lo añadimos al final de la carta de Discord.

# 5. ¡ENVIAR ALERTA!
# El robot nos manda el informe completo al móvil (Discord).
print("\n📨 Enviando informe a Discord...")
boca.enviar_alerta(mensaje_discord)
