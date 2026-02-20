# nucleo/social.py
# ESTOS SON LOS OJOS DEL ROBOT EN INTERNET
# Sirve para leer noticias

import requests  # Herramienta para navegar por internet
from bs4 import BeautifulSoup  # Herramienta para leer el código de las webs (la sopa de letras)
import random  # Herramienta para elegir cosas al azar

class OjosInternet:
    def __init__(self):
        """Constructor: Se pone las gafas para leer."""
        print("👀 INICIANDO OJOS SOCIALES (NOTICIAS)...")  # Avisamos que activamos los ojos
        # Usamos una lista de sitios web de noticias financieras
        self.fuentes = [
            "https://finance.yahoo.com/rss/",  # Noticias de Yahoo
            "https://www.coindesk.com/arc/outboundfeeds/rss/"  # Noticias de Cripto
        ]

    def leer_titulares(self):
        """Busca las letras grandes de las noticias."""
        titulares_encontrados = []  # Creamos una lista vacía para guardar titulares
        
        try:
            # Elegimos una fuente (url) al azar de nuestra lista
            url = random.choice(self.fuentes)
            print(f"🔎 Leyendo noticias de: {url} ...")  # Avisamos de dónde leemos
            
            # Nos disfrazamos de navegador normal (Mozilla) para que no nos bloqueen
            headers = {'User-Agent': 'Mozilla/5.0'}
            # Pedimos la página web y esperamos máximo 10 segundos
            respuesta = requests.get(url, headers=headers, timeout=10)
            
            if respuesta.status_code == 200:  # Si la web nos responde "OK" (200)...
                # Usamos BeautifulSoup para entender el contenido XML/HTML
                sopa = BeautifulSoup(respuesta.content, features="xml")
                # Buscamos todas las etiquetas que digan 'item' (cada noticia)
                items = sopa.find_all('item')
                
                # Cogemos solo los primeros 5 elementos encontrados
                for item in items[:5]:
                    titulo = item.title.text  # Sacamos el texto del título
                    titulares_encontrados.append(titulo)  # Lo guardamos en nuestra lista
            else:
                print("⚠️ La página web no me deja entrar.")  # Si no es 200, algo falló
                
        except Exception as e:  # Si ocurre un error inesperado...
            print(f"❌ Se me cayeron las gafas: {e}")  # Avisamos del error

        if not titulares_encontrados:  # Si la lista sigue vacía...
            return "No hay noticias importantes ahora mismo."  # Devolvemos mensaje vacío
            
        # Unimos todos los titulares con una barrita separadora
        return " | ".join(titulares_encontrados)

# Prueba rápida
if __name__ == "__main__":  # Si ejecutamos este archivo directamente...
    ojos = OjosInternet()  # Creamos los ojos
    noticias = ojos.leer_titulares()  # Leemos noticias
    print(f"📰 ÚLTIMAS NOTICIAS: {noticias}")  # Las mostramos
