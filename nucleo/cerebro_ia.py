# nucleo/cerebro_ia.py
# ESTE ES EL NUEVO CEREBRO AGENTE DE ZEROX (LANGCHAIN EDITION)
# Ahora ZEROX no es solo un script, es un AGENTE AUTÓNOMO.
# Puede usar herramientas (Internet, Calculadora) antes de tomar una decisión.

import os  # Para hablar con el sistema operativo
import json  # Para leer datos en formato JSON
from langchain_groq import ChatGroq  # El cerebro principal (Groq + LangChain)
from langchain.agents import AgentExecutor, create_react_agent  # El cuerpo del agente
from langchain_community.tools import DuckDuckGoSearchResults  # Herramienta: Ojos para ver internet
from langchain.tools import tool  # Para crear nuestras propias herramientas
from langchain_core.prompts import PromptTemplate  # Para darle instrucciones al agente

# Importamos la configuración para saber las claves secretas
try:
    import config
except ImportError:
    # Truco por si probamos este archivo suelto
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import config

# --- DEFINICIÓN DE HERRAMIENTAS (LO QUE EL ROBOT PUEDE USAR) ---

@tool
def calculadora_riesgo(capital_total: float, precio_entrada: float, stop_loss: float) -> str:
    """
    Calcula cuántas criptomonedas comprar basándose en el riesgo.
    Úsalo SIEMPRE antes de decidir una compra.
    Fórmula: (Capital * Riesgo) / (Entrada - StopLoss)
    Asume un riesgo del 2% por operación.
    """
    try:
        riesgo_por_operacion = 0.02  # Arriesgamos solo el 2% del dinero
        dinero_en_riesgo = float(capital_total) * riesgo_por_operacion
        distancia_stop = float(precio_entrada) - float(stop_loss)
        
        if distancia_stop <= 0:
            return "ERROR: El Stop Loss debe ser menor que el precio de entrada para compras (LONG)."
            
        tamano_posicion = dinero_en_riesgo / distancia_stop
        return f"CÁLCULO REALIZADO: Con {capital_total} USDT y riesgo 2%, puedes comprar {tamano_posicion:.4f} unidades."
    except Exception as e:
        return f"ERROR CÁLCULO: {e}"

# --- CLASE PRINCIPAL DEL CEREBRO ---

class CerebroAgente:
    def __init__(self):
        """
        Constructor: Aquí montamos el robot pieza a pieza.
        """
        print("🤖 ENSAMBLANDO AGENTE AUTÓNOMO (LANGCHAIN + GROQ)...")
        
        # 1. El Cerebro (LLM)
        # Usamos ChatGroq porque es rapidísimo y gratuito
        if not config.GROQ_API_KEY:
            print("❌ FALTA LA CLAVE DE GROQ. El agente no puede nacer.")
            self.agente_ejecutor = None
            return

        self.llm = ChatGroq(
            temperature=0,  # 0 = Robot serio y preciso. 1 = Robot poeta loco.
            groq_api_key=config.GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile"  # El modelo más potente disponible
        )

        # 2. Las Herramientas (Cinturón de utilidades)
        # DuckDuckGo: Para buscar noticias en tiempo real
        busqueda_internet = DuckDuckGoSearchResults()
        
        # Lista de herramientas disponibles para el agente
        self.herramientas = [busqueda_internet, calculadora_riesgo]

        # 3. Las Instrucciones (El Prompt del Sistema)
        # Aquí le decimos quién es y cómo debe comportarse.
        template = '''Responde a las siguientes preguntas lo mejor que puedas. Tienes acceso a las siguientes herramientas:

{tools}

Usa el siguiente formato:

Question: la pregunta de entrada que debes responder
Thought: siempre debes pensar qué hacer
Action: la acción a realizar, debe ser una de [{tool_names}]
Action Input: la entrada para la acción
Observation: el resultado de la acción
... (este pensamiento/acción/observación puede repetirse N veces)
Thought: ahora sé la respuesta final
Final Answer: la respuesta final a la pregunta de entrada original

Pregunta: {input}
Pensamiento: {agent_scratchpad}'''

        prompt = PromptTemplate.from_template(template)

        # 4. Crear el Agente (ReAct)
        # ReAct = Reason + Act (Razonar y Actuar)
        agente = create_react_agent(self.llm, self.herramientas, prompt)

        # 5. El Ejecutor (El cuerpo que mueve al agente)
        # handle_parsing_errors=True es vital: si el LLM se lía con el formato, LangChain lo corrige.
        self.agente_ejecutor = AgentExecutor(
            agent=agente, 
            tools=self.herramientas, 
            verbose=True,  # Para ver en consola qué está pensando
            handle_parsing_errors=True
        )
        print("✅ Agente Autónomo operativo y listo para operar.")

    def tomar_decision(self, datos_mercado, saldo_actual):
        """
        Función maestra: Le damos datos y el agente decide qué hacer.
        """
        if not self.agente_ejecutor:
            return "ERROR_SISTEMA"

        # Preparamos la misión para el agente
        mision = f"""
        ACTÚA COMO UN TRADER PROFESIONAL. Tienes estos datos del mercado:
        {datos_mercado}
        
        Tu saldo actual es: {saldo_actual} USDT.
        
        PASOS OBLIGATORIOS:
        1. Analiza los datos técnicos.
        2. Si tienes dudas, busca en internet "Bitcoin news last hour" usando la herramienta de búsqueda.
        3. Si decides comprar, CALCULA PRIMERO el tamaño de la posición usando la calculadora (Stop Loss sugerido: 1% abajo del precio).
        4. DECISIÓN FINAL: Debes terminar diciendo una sola palabra: COMPRA, VENTA o ESPERA.
        """

        try:
            # ¡Acción! El agente empieza a pensar y usar herramientas
            respuesta = self.agente_ejecutor.invoke({"input": mision})
            
            # Limpiamos la respuesta final
            decision_texto = respuesta['output'].strip().upper()
            
            if "COMPRA" in decision_texto: return "COMPRA"
            if "VENTA" in decision_texto: return "VENTA"
            return "ESPERA"

        except Exception as e:
            print(f"⚠️ El agente se confundió: {e}")
            return "ESPERA"

# Pequeña prueba si ejecutamos este archivo directamente
if __name__ == "__main__":
    cerebro = CerebroAgente()
    
    # Datos falsos para ver si busca en internet y calcula
    datos_fake = "BTC/USDT Precio: 65000. RSI: 35 (Bajo). Tendencia: Lateral."
    saldo_fake = 1000
    
    print("\n🏁 INICIANDO PRUEBA DE CAMPO...")
    decision = cerebro.tomar_decision(datos_fake, saldo_fake)
    print(f"\n📢 DECISIÓN DEL AGENTE: {decision}")
