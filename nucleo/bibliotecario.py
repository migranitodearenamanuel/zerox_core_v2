# nucleo/bibliotecario.py
# 📚 EL MINERO DE CONOCIMIENTO (EXTRACTOR DE ESTRATEGIAS)
# Este agente lee los libros de Bulkowski y Nison para encontrar patrones ganadores.

import json  # Para escribir las recetas en un formato que todos entiendan.
import os    # Para ver los archivos en la carpeta.
import random # (Temporal) Simulamos que leemos libros complejos.

class BibliotecarioRAG:
    def __init__(self):
        # Cuando el bibliotecario despierta, saluda.
        print("📚 Bibliotecario: Listo para buscar patrones de velas y figuras en los libros.")
        self.archivo_salida = "estrategias_candidatas.json"

    def analizar_patrones_tecnicos(self):
        """
        Escanea la biblioteca buscando sabiduría ancestral sobre gráficos.
        Busca específicamente patrones de Velas Japonesas (Nison) y Figuras Chartistas (Bulkowski).
        """
        print("📚 Bibliotecario: Leyendo 'Japanese Candlestick Charting Techniques'...")
        print("📚 Bibliotecario: Leyendo 'Encyclopedia of Chart Patterns'...")

        # Simulamos que hemos extraído estas reglas lógicas de los textos.
        # En una versión futura con IA real, esto leería el PDF párrafo a párrafo.
        
        estrategias_extraidas = [
            {
                "nombre": "PATRON_NISON_ENGULFING_ALCISTA",
                "tipo": "REVERSION", # Apostar a que el precio da la vuelta.
                "reglas": {
                    "descripcion": "Una vela roja pequeña seguida de una vela verde gigante que se la come.",
                    "vela_1": "ROJA",
                    "vela_2": "VERDE",
                    "condicion_cuerpo": "CUERPO_2 > CUERPO_1", # La segunda es más grande.
                    "condicion_cierre": "CIERRE_2 > APERTURA_1", # Cierra por encima de donde abrió la primera.
                    "tendencia_previa": "BAJISTA" # Tiene que venir cayendo.
                },
                "fuente": "Steve Nison - Japanese Candlestick Charting"
            },
            {
                "nombre": "PATRON_BULKOWSKI_DOBLE_SUELO",
                "tipo": "FIGURA_W", # Forma de letra W.
                "reglas": {
                    "descripcion": "El precio toca el suelo dos veces y no puede romperlo.",
                    "puntos_minimos": 2, # Dos toques abajo.
                    "distancia_tiempo": "10_VELAS_MINIMO", # Separados por un tiempo.
                    "diferencia_precio": "MENOR_AL_2%", # Los dos suelos están casi al mismo precio.
                    "volumen": "CRECIENTE_EN_SUBIDA" # La gente compra con ganas al final.
                },
                "fuente": "Thomas Bulkowski - Encyclopedia of Chart Patterns"
            },
            {
                "nombre": "PATRON_NISON_MARTILLO",
                "tipo": "REBOTE", # Como un martillo golpeando el suelo.
                "reglas": {
                    "descripcion": "Vela con cuerpo pequeño arriba y una sombra larga abajo.",
                    "forma": "MARTILLO",
                    "sombra_inferior": "DOS_VECES_EL_CUERPO", # La pata es larga.
                    "sombra_superior": "CASI_NULA", # Apenas tiene cabeza.
                    "tendencia_previa": "BAJISTA"
                },
                "fuente": "Steve Nison"
            }
        ]

        print(f"📚 Bibliotecario: ¡Eureka! He encontrado {len(estrategias_extraidas)} patrones mágicos.")
        
        # Guardamos el hallazgo en el archivo JSON.
        self._guardar_estrategias(estrategias_extraidas)
        return estrategias_extraidas

    def _guardar_estrategias(self, datos):
        """
        Escribe las estrategias en el disco duro para que el Laboratorio las use.
        """
        try:
            with open(self.archivo_salida, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            print(f"📚 Bibliotecario: Recetas guardadas en '{self.archivo_salida}'.")
        except Exception as e:
            print(f"📚 Error guardando archivo: {e}")

# Prueba rápida.
if __name__ == "__main__":
    biblio = BibliotecarioRAG()
    biblio.analizar_patrones_tecnicos()
