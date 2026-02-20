import os  # Traigo la herramienta para ver las carpetas de mi ordenador

# Aquí pongo el nombre del archivo gigante donde voy a guardar todo
nombre_archivo_salida = "PROYECTO_COMPLETO_ZEROX.txt"

# Aquí hago una lista de las carpetas a las que NO quiero entrar
carpetas_prohibidas = ["venv", "__pycache__", ".git", ".idea", ".vscode"]

# Aquí digo qué tipos de archivos sí quiero guardar (solo los de texto y código)
tipos_de_archivo_permitidos = (".py", ".md", ".txt", ".env", ".json")

# Empiezo a crear el archivo gigante nuevo (la "w" es de escribir en inglés, write)
# Uso encoding="utf-8" para que entienda las tildes y letras raras
with open(nombre_archivo_salida, "w", encoding="utf-8") as archivo_gigante:
    
    # Escribo un título bonito al principio del archivo gigante
    archivo_gigante.write("=== AQUI ESTA TODO EL PROYECTO ZEROX ===

")

    # Empiezo a caminar por todas las carpetas, paso a paso (os.walk ayuda a caminar)
    # carpeta_actual es donde estoy ahora
    # subcarpetas son las carpetas dentro de donde estoy
    # archivos son las hojas sueltas que hay aquí
    for carpeta_actual, subcarpetas, archivos in os.walk("."):
        
        # Antes de seguir, quito de la lista las carpetas prohibidas para no entrar en ellas
        # Esto hace que si veo "venv", me la salto y no miro lo que hay dentro
        subcarpetas[:] = [c for c in subcarpetas if c not in carpetas_prohibidas]

        # Ahora miro uno por uno todos los archivos que encontré en esta carpeta
        for archivo in archivos:
            
            # Pregunto: ¿Este archivo termina con alguna de las terminaciones permitidas?
            if archivo.endswith(tipos_de_archivo_permitidos):
                
                # Si es un archivo bueno, calculo su dirección completa
                # (ejemplo: nucleo/sentidos.py)
                ruta_del_archivo = os.path.join(carpeta_actual, archivo)
                
                # Me aseguro de no copiar el mismo archivo gigante dentro de sí mismo
                if archivo == nombre_archivo_salida:
                    continue  # Si soy yo, me salto y sigo con el siguiente

                # Intento leer el archivo pequeño (uso try por si falla algo)
                try:
                    # Abro el archivo pequeño para solo leer (la "r" es de read)
                    # Uso errors="ignore" para que si hay una letra rara no se rompa nada
                    with open(ruta_del_archivo, "r", encoding="utf-8", errors="ignore") as archivo_pequeno:
                        # Leo todo lo que hay dentro y lo guardo en la memoria
                        contenido = archivo_pequeno.read()

                    # Ahora escribo en mi archivo gigante la cabecera
                    archivo_gigante.write(f"--- ARCHIVO: {ruta_del_archivo} ---
")
                    
                    # Pego todo el contenido que leí del archivo pequeño
                    archivo_gigante.write(contenido + "
")
                    
                    # Pongo una línea final para saber que este archivo terminó
                    archivo_gigante.write("--- FIN DE ARCHIVO ---

")
                    
                    # Escribo en la pantalla negra que todo salió bien con este archivo
                    print(f"He guardado: {ruta_del_archivo}")

                # Si algo sale mal al leer el archivo (está roto o cerrado con llave)
                except Exception as error:
                    # Aviso en la pantalla negra que hubo un problema
                    print(f"Uy, no pude leer {ruta_del_archivo}: {error}")

# Cuando termino de caminar por todas las carpetas, aviso que acabé
print("
¡Misión cumplida! Todo el proyecto está en el archivo gigante.")
