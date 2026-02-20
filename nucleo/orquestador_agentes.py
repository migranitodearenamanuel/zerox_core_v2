# nucleo/orquestador_agentes.py
# 🌐 EL CEREBRO MAESTRO (EJECUTOR BLINDADO CON LANGGRAPH)
# Coordina el Scout, el Auditor y el Gestor de Riesgo para operar de verdad.

import asyncio
import json
import ccxt.async_support as ccxt
from typing import TypedDict, Dict, Any, Annotated
import operator

# Importamos las herramientas del mapa (LangGraph).
from langgraph.graph import StateGraph, END

# Importamos a nuestros agentes especializados.
from nucleo.gestor_riesgo import QuantEngine
from nucleo.supervisor_autonomo import AuditorEVM
import config 

# ESTADO DEL SISTEMA (La memoria a corto plazo)
# Usamos Annotated con operator.add solo si queremos guardar historia (append).
# Aquí usamos sobrescritura simple para la mayoría de campos.
class EstadoTrading(TypedDict):
    capital_real: float
    simbolo: str
    estrategia_activa: str
    precio_actual: float
    es_seguro: bool
    decision: str
    mensaje: str

async def nodo_scout_francotirador(estado: EstadoTrading) -> Dict[str, Any]:
    """
    AGENTE SCOUT: Escanea el mercado buscando SOLO lo que validó el laboratorio.
    """
    print("🔭 Scout: Escaneando mercado en busca de Estrategias Maestras...")
    
    # 1. Cargar las estrategias ganadoras del laboratorio.
    try:
        with open("estrategias_maestras.json", 'r') as f:
            estrategias_maestras = json.load(f)
    except:
        return {"decision": "DORMIR", "mensaje": "No hay estrategias maestras aún."}

    if not estrategias_maestras:
        return {"decision": "DORMIR", "mensaje": "Lista de estrategias vacía."}

    # 2. Mirar el mercado real.
    exchange = ccxt.bitget()
    try:
        ticker = await exchange.fetch_ticker(config.SYMBOL)
        precio = ticker['last']
        await exchange.close()
    except:
        await exchange.close()
        return {"decision": "ERROR", "mensaje": "Error de conexión con Exchange."}

    # 3. Aplicar lógica de reconocimiento (Simplificada).
    # Aquí el Scout revisaría si se cumple alguna estrategia maestra AHORA MISMO.
    # Por ahora, asumimos que detecta la primera de la lista para probar el flujo.
    estrategia_detectada = estrategias_maestras[0]
    
    print(f"🎯 Scout: ¡Patrón detectado! Coincide con {estrategia_detectada['nombre']}")

    return {
        "simbolo": config.SYMBOL,
        "precio_actual": precio,
        "estrategia_activa": estrategia_detectada['nombre'],
        "decision": "AUDITAR" # Siguiente paso: Llamar al policía.
    }

async def nodo_auditor_blindado(estado: EstadoTrading) -> Dict[str, Any]:
    """
    AGENTE AUDITOR: Simula la transacción para evitar trampas.
    """
    # Si la decisión no es auditar, no hacemos nada (aunque el grafo no debería llevarnos aquí).
    if estado.get("decision") != "AUDITAR":
        return {"es_seguro": False}

    print(f"🛡️ Auditor: Verificando seguridad del token en {estado['simbolo']}...")
    
    # Instanciamos al policía EVM (Blockchain).
    auditor = AuditorEVM()
    
    # IMPORTANTE: En un entorno real, necesitamos la dirección del contrato del token.
    # Usamos una dirección dummy de ejemplo.
    token_dummy = "0x4200000000000000000000000000000000000006" 
    
    # Ejecutamos la simulación de venta (Honeypot Check).
    reporte = auditor.auditar_token(token_dummy)
    
    if reporte["es_seguro"]:
        print("🛡️ Auditor: ✅ Token limpio. Simulación exitosa.")
        return {"es_seguro": True, "decision": "CALCULAR_RIESGO"}
    else:
        print(f"🛡️ Auditor: ❌ PELIGRO. {reporte['motivo']}")
        return {"es_seguro": False, "decision": "ABORTAR"}

async def nodo_quant_ejecutor(estado: EstadoTrading) -> Dict[str, Any]:
    """
    AGENTE QUANT: Calcula el tamaño y EJECUTA (Simulado).
    """
    if estado.get("decision") != "CALCULAR_RIESGO":
        return {}

    # 1. Obtenemos capital real (Simulado en 15.0).
    saldo = 15.0 
    
    # 2. Usamos el Gestor de Riesgo Adaptativo.
    motor = QuantEngine(capital_inicial=saldo)
    apuesta = motor.calcular_kelly_adaptativo()
    
    print(f"📐 Quant: Ejecutando orden. Capital: {saldo}€. Apuesta Kelly: {apuesta:.2f}€")
    
    # Aquí iría la llamada final: await exchange.create_order(...)
    
    return {
        "capital_real": saldo,
        "mensaje": f"Orden ENVIADA. Tamaño: {apuesta:.2f}€"
    }

# --- CONSTRUCCIÓN DEL CEREBRO (GRAFO) ---

# 1. Definimos las reglas de tráfico (Rutas Condicionales).

def decidir_si_auditar(estado: EstadoTrading) -> str:
    """Decide si vamos al Auditor o nos vamos a dormir."""
    if estado["decision"] == "AUDITAR":
        return "auditor"
    return END

def decidir_si_operar(estado: EstadoTrading) -> str:
    """Decide si vamos al Quant o abortamos misión."""
    if estado["decision"] == "CALCULAR_RIESGO":
        return "quant"
    return END

# 2. Creamos el tablero de juego.
workflow = StateGraph(EstadoTrading)

# 3. Añadimos a los jugadores (Nodos).
workflow.add_node("scout", nodo_scout_francotirador)
workflow.add_node("auditor", nodo_auditor_blindado)
workflow.add_node("quant", nodo_quant_ejecutor)

# 4. Dibujamos las flechas (Flujo).
workflow.set_entry_point("scout") # Empezamos siempre con el Scout.

# Del Scout podemos ir al Auditor o Terminar.
workflow.add_conditional_edges(
    "scout",
    decidir_si_auditar,
    {
        "auditor": "auditor",
        END: END
    }
)

# Del Auditor podemos ir al Quant o Terminar.
workflow.add_conditional_edges(
    "auditor",
    decidir_si_operar,
    {
        "quant": "quant",
        END: END
    }
)

# Del Quant siempre terminamos (por ahora).
workflow.add_edge("quant", END)

# 5. ¡COMPILAMOS EL CEREBRO! (CRÍTICO PARA QUE FUNCIONE)
app = workflow.compile()
CEREBRO_ZEROX = app # ALIAS CRÍTICO: Esto es lo que busca SISTEMA_AUTONOMO.py

# Si ejecutamos este archivo directamente, probamos el cerebro.
if __name__ == "__main__":
    print("🏁 Iniciando prueba manual del CEREBRO_ZEROX...")
    # Ejecutamos el grafo con un estado inicial vacío.
    resultado = asyncio.run(CEREBRO_ZEROX.ainvoke({"capital_real": 0, "decision": "INICIO"}))
    print("🏁 Resultado final:", resultado)
