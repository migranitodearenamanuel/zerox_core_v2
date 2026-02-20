# auto_evolucion.py
# ESTE ES EL GENETISTA DIGITAL (EL MÉDICO DEL CÓDIGO)
# Se encarga de curar al robot si se pone enfermo (errores)
# y de hacerlo más fuerte si pierde dinero.
# 1. Lee los diarios de errores (logs).
# 2. Si encuentra fallos, pide ayuda a Groq para reescribir el código.
# 3. Guarda los cambios (Git) y reinicia el cerebro.

import os
import sys
import json
import time
import subprocess
from groq import Groq

# Importamos la configuración para saber las claves secretas
try:
    import config
except ImportError:
    # Si estamos ejecutando este archivo solo para probar, intentamos importar desde arriba
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import config

class GenetistaDigital:
    def __init__(self):
        """
        Constructor: Prepara al médico para operar.
        """
        print("🧬 INICIANDO GENETISTA DIGITAL (AUTO-MEJORA)...")
        
        # Necesitamos a Groq para que nos escriba el código nuevo
        try:
            self.cliente_groq = Groq(api_key=config.GROQ_API_KEY)
            print("✅ Groq listo para operar código (Cirujano de Software).")
        except Exception as e:
            print(f"❌ Error al llamar al cirujano Groq: {e}")
            self.cliente_groq = None

        # Rutas de archivos importantes
        self.ruta_logs = "logs/errores.log"
        self.ruta_estado = "estado_bot.json"
        
        # Aseguramos que exista la carpeta de logs
        if not os.path.exists("logs"):
            os.makedirs("logs")

    def leer_errores(self):
        """
        Lee el diario de errores para ver si algo ha dolido.
        Devuelve el último error grave encontrado.
        """
        if not os.path.exists(self.ruta_logs):
            return None
        
        try:
            with open(self.ruta_logs, "r", encoding="utf-8") as f:
                lineas = f.readlines()
                if not lineas:
                    return None
                # Devolvemos las últimas 20 líneas, que es lo más fresco
                return "".join(lineas[-20:])
        except Exception:
            return None

    def solicitar_correccion_groq(self, codigo_actual, error_detectado):
        """
        Esta función envía el código roto y el error a Groq.
        Groq nos devuelve el código ARREGLADO.
        """
        if not self.cliente_groq:
            return None

        prompt = f"""
        ACTÚA COMO UN INGENIERO DE SOFTWARE SENIOR EXPERTO EN PYTHON.
        Tengo un script que está fallando.
        
        ERROR REPORTADO:
        {error_detectado}
        
        CÓDIGO ACTUAL (CON FALLOS):
        ```python
        {codigo_actual}
        ```
        
        TU MISIÓN:
        1. Analiza por qué falla.
        2. Reescribe el código ENTERO corrigiendo el error.
        3. Mantén los comentarios originales y añade nuevos explicando el arreglo.
        4. NO EXPLIQUES NADA FUERA DEL CÓDIGO. Solo devuelve el bloque de código Python listo para guardar.
        """

        try:
            # Pedimos la cura a Groq
            respuesta = self.cliente_groq.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Eres un sistema de auto-reparación de código. Solo respondes con código Python válido."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.2, # Creatividad baja para no inventar cosas raras
            )
            
            # Extraemos el código de la respuesta
            contenido = respuesta.choices[0].message.content
            
            # Limpiamos los bloques de markdown si los pone (```python ... ```)
            if "```python" in contenido:
                contenido = contenido.split("```python")[1].split("```")[0]
            elif "```" in contenido:
                contenido = contenido.split("```")[1].split("```")[0]
                
            return contenido.strip()

        except Exception as e:
            print(f"⚠️ Groq no pudo operar al paciente: {e}")
            return None

    def aplicar_parche(self, archivo_afectado, nuevo_codigo):
        """
        Sobrescribe el archivo viejo con el nuevo código mejorado.
        ¡CUIDADO! Esto es cirugía a corazón abierto.
        """
        try:
            with open(archivo_afectado, "w", encoding="utf-8") as f:
                f.write(nuevo_codigo)
            print(f"✅ Parche aplicado con éxito en: {archivo_afectado}")
            return True
        except Exception as e:
            print(f"❌ Fallo al aplicar el parche: {e}")
            return False

    def auto_commit_push(self, mensaje_commit):
        """
        Sube los cambios a la nube (GitHub) para no perder la mejora.
        Es como guardar la partida después de vencer a un jefe.
        """
        try:
            # 1. Añadimos el archivo al carrito (git add)
            subprocess.run(["git", "add", "."], check=True)
            
            # 2. Confirmamos la compra (git commit)
            subprocess.run(["git", "commit", "-m", f"AUTO-FIX: {mensaje_commit}"], check=True)
            
            # 3. Enviamos a la nube (git push)
            # Nota: Esto requiere que las credenciales estén configuradas en el entorno
            subprocess.run(["git", "push"], check=True)
            
            print("☁️ Mejoras subidas a GitHub correctamente.")
            return True
        except Exception as e:
            print(f"⚠️ No se pudo subir a GitHub (¿faltan permisos?): {e}")
            return False

    def reiniciar_sistema(self):
        """
        Reinicia el programa entero para que los cambios surtan efecto.
        Es como apagar y encender el ordenador.
        """
        print("🔄 REINICIANDO SISTEMA PARA APLICAR MEJORAS...")
        time.sleep(2) # Damos tiempo a leer el mensaje
        
        # Magia de Python para reiniciarse a sí mismo
        os.execv(sys.executable, ['python'] + sys.argv)

    def evolucionar(self):
        """
        FUNCIÓN PRINCIPAL.
        Busca errores, pide arreglos, aplica parches y reinicia.
        """
        print("\n🔎 Buscando enfermedades en el código...")
        
        # 1. Buscamos errores recientes
        error = self.leer_errores()
        
        if error:
            print(f"🚨 ¡ERROR ENCONTRADO!\n{error}")
            
            # Intentamos adivinar qué archivo falló buscando ".py" en el error
            archivo_sospechoso = "nucleo/cerebro_ia.py" # Por defecto
            
            # Buscamos nombres de archivos en el log
            import re
            match = re.search(r'File "([^"]+\.py)"', error)
            if match:
                posible_archivo = match.group(1)
                # Solo aceptamos archivos que existen
                if os.path.exists(posible_archivo):
                    archivo_sospechoso = posible_archivo
                    print(f"🕵️ Detectado archivo culpable: {archivo_sospechoso}")
            
            # Leemos el código actual
            try:
                with open(archivo_sospechoso, "r", encoding="utf-8") as f:
                    codigo_viejo = f.read()
            except:
                print("No pude leer el archivo sospechoso.")
                return

            # 2. Pedimos ayuda al doctor Groq
            print("🚑 Llamando a Groq para reparación de emergencia...")
            codigo_nuevo = self.solicitar_correccion_groq(codigo_viejo, error)
            
            if codigo_nuevo:
                # 3. Aplicamos la medicina
                if self.aplicar_parche(archivo_sospechoso, codigo_nuevo):
                    # 4. Guardamos en el historial (Git)
                    self.auto_commit_push("Corrección automática de error crítico")
                    
                    # 5. Reiniciamos
                    self.reiniciar_sistema()
            else:
                print("😔 Groq no pudo arreglarlo esta vez.")
        
        else:
            print("✨ El sistema está sano. No hay errores graves.")
            # Aquí podríamos mirar el PnL y ver si perdemos dinero para cambiar la estrategia
            # pero por ahora nos centramos en que no crashee.

# Prueba rápida
if __name__ == "__main__":
    medico = GenetistaDigital()
    # Simular un chequeo
    medico.evolucionar()
