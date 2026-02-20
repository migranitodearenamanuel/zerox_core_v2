# SISTEMA_AUTONOMO.py
# 🚀 EL CORAZÓN DE ZEROX (SISTEMA DE ALTA FRECUENCIA)
# Este archivo es el jefe que nunca duerme.
# Cambia su velocidad: corre mucho si hay peligro, y descansa si no pasa nada.

import time  # Para saber la hora.
import json  # Para leer la memoria del robot.
import asyncio  # Para hacer varias cosas a la vez (asíncrono).
from datetime import datetime  # Para saber el día exacto.

# Importamos el cerebro y la boca del robot.
from nucleo.orquestador_agentes import CEREBRO_ZEROX  # El cerebro inteligente.
from nucleo.sentidos import Comunicador  # La boca para hablar por Discord.
import config  # Las instrucciones secretas.

def cargar_estado():
    """
    Lee el archivo 'estado_bot.json' para recordar qué estaba haciendo.
    Es como leer un diario al despertarse.
    """
    try:
        # Intentamos abrir el archivo de memoria.
        with open("estado_bot.json", "r") as f:
            return json.load(f)  # Devuelve lo que recuerda.
    except FileNotFoundError:
        # Si no encuentra el diario, empieza de cero con 15 euros y sin posiciones.
        return {"capital": 15.0, "posiciones": []}

def guardar_estado(estado):
    """
    Escribe en el diario lo que ha pasado para no olvidarlo.
    """
    # Abrimos el archivo para escribir (w = write).
    with open("estado_bot.json", "w") as f:
        json.dump(estado, f, indent=4)  # Lo guarda bonito y ordenado.

async def ciclo_vida():
    """
    LA RUTINA PRINCIPAL (EL ALMA DEL ROBOT).
    Aquí el robot decide si corre (Scalping) o camina (Escaneo).
    """
    print("🚀 SISTEMA ZEROX: Iniciando motores de Alta Frecuencia...")
    
    # Preparamos la boca para hablar.
    comunicador = Comunicador()
    comunicador.enviar_alerta("🟢 ZEROX ONLINE: Sistema de Frecuencia Dinámica activado.")

    # Bucle Infinito: Esto no para nunca.
    while True:
        try:
            # 1. Miramos la hora.
            ahora = datetime.now().strftime("%H:%M:%S")
            
            # 2. Leemos la memoria para saber si tenemos dinero en juego.
            memoria = cargar_estado()
            
            # Buscamos si hay algo en la lista de "posiciones" (inversiones abiertas).
            # Si la lista tiene cosas (len > 0), es que estamos jugando.
            tengo_posiciones = len(memoria.get("posiciones", [])) > 0

            # 3. DECIDIMOS LA VELOCIDAD (FRECUENCIA DINÁMICA).
            if tengo_posiciones:
                # MODO PÁNICO (GUEPARDO): Hay dinero en riesgo. ¡Corremos!
                tiempo_dormir = 10  # Solo dormimos 10 segundos.
                modo = "🐆 MODO GUEPARDO (Vigilancia Extrema)"
                orden_cerebro = "GESTIONAR_POSICION" # Le decimos al cerebro que vigile.
            else:
                # MODO AHORRO (TORTUGA): Estamos líquidos. Buscamos tranquilos.
                tiempo_dormir = 900  # Dormimos 15 minutos (900 segundos).
                modo = "🐢 MODO TORTUGA (Escaneo de Mercado)"
                orden_cerebro = "INICIO" # Le decimos al cerebro que busque algo nuevo.

            print(f"\n⏰ {ahora} - {modo}")

            # 4. PREPARAMOS LOS DATOS PARA EL CEREBRO.
            inputs = {
                "capital_real": memoria.get("capital", 15.0), # Cuánto dinero tenemos.
                "decision": orden_cerebro, # Qué queremos que haga.
                "posiciones": memoria.get("posiciones", []) # Le pasamos las inversiones actuales.
            }

            # 5. EJECUTAR EL CEREBRO (PENSAR).
            # Usamos 'await' porque el cerebro es asíncrono.
            print(f"🧠 Cerebro: Ejecutando orden '{orden_cerebro}'...")
            resultado = await CEREBRO_ZEROX.ainvoke(inputs)
            
            # 6. Analizar la respuesta.
            ultima_accion = resultado.get("mensaje", "Sin novedad")
            decision_final = resultado.get("decision", "NADA")

            print(f"🤖 Resultado: {decision_final} -> {ultima_accion}")

            # 7. Si pasó algo importante, avisamos por Discord.
            if decision_final in ["CALCULAR_RIESGO", "AUDITAR", "CERRAR_POSICION", "ABORTAR"]:
                 comunicador.enviar_alerta(f"📢 {modo}: {ultima_accion}")

            # 8. Guardamos los cambios en la memoria.
            # Si el cerebro nos devuelve un capital nuevo o posiciones nuevas, actualizamos.
            cambios_importantes = False
            if "capital_real" in resultado:
                memoria["capital"] = resultado["capital_real"]
                cambios_importantes = True
            if "posiciones" in resultado: # Si el cerebro abre/cierra posiciones.
                memoria["posiciones"] = resultado["posiciones"]
                cambios_importantes = True
            
            if cambios_importantes:
                guardar_estado(memoria)

            # 9. A DORMIR.
            print(f"💤 Durmiendo {tiempo_dormir} segundos...")
            await asyncio.sleep(tiempo_dormir)

        except KeyboardInterrupt:
            # Si pulsamos Ctrl+C para apagarlo.
            print("\n🛑 APAGANDO SISTEMA...")
            comunicador.enviar_alerta("🔴 ZEROX OFF: Sistema detenido manualmente.")
            break 
            
        except Exception as e:
            # Si el robot se marea (Error).
            error_msg = f"⚠️ ERROR CRÍTICO: {str(e)}"
            print(error_msg)
            try:
                comunicador.enviar_alerta(error_msg)
            except:
                pass # Si no hay internet, no hacemos nada.
            
            # Si hay error, esperamos 1 minuto y probamos otra vez.
            print("🔄 Reiniciando en 60 segundos...")
            await asyncio.sleep(60)

# PUNTO DE ARRANQUE.
if __name__ == "__main__":
    # Arrancamos el bucle asíncrono.
    try:
        asyncio.run(ciclo_vida())
    except KeyboardInterrupt:
        pass
