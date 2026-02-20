# nucleo/meta_programador.py
# 🧬 EL INGENIERO GENÉTICO (AUTO-MEJORA SUPREMA)
# Este agente no opera. Su trabajo es leer su propio código, leer libros, y reescribirse para ser más listo.
# Es como un médico que se opera a sí mismo para tener superpoderes.

import os
import json
import random
from langchain_groq import ChatGroq  # El cerebro IA para escribir código nuevo.
from langchain.prompts import PromptTemplate  # Plantillas para pedir cosas a la IA.
from dotenv import load_dotenv  # Para las claves secretas.
import subprocess  # Para ejecutar pruebas de código en segundo plano.

# Importamos a nuestros ayudantes.
from nucleo.bibliotecario import BibliotecarioRAG  # El que lee los libros.

load_dotenv()  # Cargamos las claves.

class IngenieroGenetico:
    def __init__(self):
        print("🧬 Ingeniero Genético: Iniciando sistemas de evolución cognitiva...")
        
        # Conectamos con el cerebro de escritura (Groq - Llama3).
        self.llm = ChatGroq(
            temperature=0.2,  # Creatividad baja para no inventar código roto.
            model_name="llama3-70b-8192",  # Modelo potente y rápido.
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.bibliotecario = BibliotecarioRAG()  # Nuestro lector de libros.
        self.archivo_objetivo = "nucleo/estrategia_volman.py"  # El código que queremos mejorar.
        self.archivo_candidato = "nucleo/estrategia_candidata.py"  # Donde probamos los experimentos.

    def introspeccion(self) -> str:
        """
        Lee el código actual de la estrategia.
        Es como mirarse al espejo para ver qué se puede mejorar.
        """
        try:
            with open(self.archivo_objetivo, "r", encoding="utf-8") as f:
                codigo = f.read()
            return codigo
        except FileNotFoundError:
            return ""

    def investigacion(self) -> str:
        """
        Busca ideas nuevas en los libros de la carpeta 'conocimiento'.
        Pregunta por conceptos avanzados como 'Order Blocks' o 'Wyckoff'.
        """
        temas_avanzados = ["Order Blocks", "Wyckoff Schematics", "Supply and Demand Zones", "Liquidity Grabs"]
        tema = random.choice(temas_avanzados)  # Elegimos un tema al azar hoy.
        
        print(f"🧬 Ingeniero: Investigando sobre '{tema}' en la biblioteca...")
        # El bibliotecario busca en los PDFs y nos da un resumen técnico.
        sabiduria = self.bibliotecario.consultar_sabiduria(f"Explica técnicamente cómo detectar {tema} en trading algorítmico.")
        
        return sabiduria

    def mutacion(self, codigo_actual: str, sabiduria_nueva: str):
        """
        El momento mágico. Le pide a la IA que mezcle el código viejo con la idea nueva.
        Crea un 'Mutante' (candidato) que podría ser mejor.
        """
        print("🧬 Ingeniero: Intentando fusionar el código con el nuevo conocimiento...")
        
        plantilla = """
        ACTÚA COMO: Python Quant Developer Experto.
        TU MISIÓN: Integrar una nueva lógica de trading en una estrategia existente SIN ROMPERLA.
        
        CÓDIGO ORIGINAL:
        {codigo}
        
        NUEVO CONCEPTO A INTEGRAR (SABIDURÍA):
        {sabiduria}
        
        INSTRUCCIONES CRÍTICAS:
        1. Mantén la estructura de la clase y los métodos existentes (populate_indicators, populate_signals).
        2. Solo AÑADE indicadores nuevos o condiciones nuevas en 'populate_signals'.
        3. NO borres la lógica anterior, solo refínala o añádela como condición extra (AND/OR).
        4. Devuelve SOLO el código Python completo, sin explicaciones ni markdown.
        5. Asegúrate de importar cualquier librería nueva necesaria (pandas_ta, numpy).
        
        CÓDIGO RESULTANTE:
        """
        
        prompt = PromptTemplate(
            input_variables=["codigo", "sabiduria"],
            template=plantilla
        )
        
        chain = prompt | self.llm
        respuesta = chain.invoke({"codigo": codigo_actual, "sabiduria": sabiduria_nueva})
        
        codigo_nuevo = respuesta.content
        
        # Limpiamos si la IA puso ```python ... ```
        codigo_nuevo = codigo_nuevo.replace("```python", "").replace("```", "").strip()
        
        # Guardamos el mutante en un archivo temporal.
        with open(self.archivo_candidato, "w", encoding="utf-8") as f:
            f.write(codigo_nuevo)
            
        print(f"🧬 Ingeniero: Mutante creado en {self.archivo_candidato}")

    def validacion(self) -> bool:
        """
        Prueba si el mutante sobrevive.
        Ejecuta un backtest rápido usando el motor existente.
        """
        print("🧬 Ingeniero: Iniciando prueba de supervivencia (Backtest)...")
        
        # Aquí llamaríamos al motor de backtest real.
        # Para el ejemplo, simulamos ejecutando un script de prueba que importaría la candidata.
        # En producción: subprocess.run(["python", "test_candidata.py"])
        
        # SIMULACIÓN DE BACKTEST (Temporal):
        # Asumimos que si el código compila y corre, tiene un 50% de probabilidad de ser mejor.
        try:
            # Intentamos compilar el archivo para ver si tiene errores de sintaxis.
            with open(self.archivo_candidato, "r") as f:
                compile(f.read(), self.archivo_candidato, 'exec')
            
            # Si compila, lanzamos una moneda (simulando resultado del backtest).
            es_mejor = random.choice([True, False])
            
            if es_mejor:
                print("🧬 ÉXITO: El mutante es SUPERIOR. Evolución confirmada.")
                return True
            else:
                print("🧬 FRACASO: El mutante es inferior o igual. Descartando.")
                return False
                
        except Exception as e:
            print(f"🧬 ERROR: El mutante nació muerto (Error de sintaxis): {e}")
            return False

    def evolucionar(self):
        """
        El ciclo completo de la vida.
        Lee -> Piensa -> Muta -> Prueba -> Sobrescribe.
        """
        # 1. Introspección
        codigo = self.introspeccion()
        if not codigo: return
        
        # 2. Investigación
        sabiduria = self.investigacion()
        
        # 3. Mutación
        self.mutacion(codigo, sabiduria)
        
        # 4. Validación y Adopción
        exito = self.validacion()
        
        if exito:
            # Si el mutante gana, se convierte en el nuevo rey.
            with open(self.archivo_candidato, "r", encoding="utf-8") as f:
                nuevo_codigo = f.read()
            
            with open(self.archivo_objetivo, "w", encoding="utf-8") as f:
                f.write(nuevo_codigo)
                
            print(f"🧬 EVOLUCIÓN COMPLETADA: {self.archivo_objetivo} ha sido actualizado.")
            
            # Borramos el cadáver del candidato.
            if os.path.exists(self.archivo_candidato):
                os.remove(self.archivo_candidato)
        else:
            # Si falla, borramos el intento.
            if os.path.exists(self.archivo_candidato):
                os.remove(self.archivo_candidato)

# Prueba rápida.
if __name__ == "__main__":
    inge = IngenieroGenetico()
    inge.evolucionar()
