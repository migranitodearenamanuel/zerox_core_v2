# nucleo/estrategia_volman.py
# 📉 EL DETECTIVE DE PATRONES (ESTRATEGIA BOB VOLMAN)
# Este archivo busca formas especiales en el gráfico de precios.
# Si ve la forma correcta, nos avisa para disparar.

import pandas as pd  # Traemos la herramienta para manejar tablas de datos (Excel gigante).
import pandas_ta as ta  # Traemos los indicadores técnicos (las reglas de medir).

class AnalistaVolman:
    """
    El ojo experto que busca los secretos de Bob Volman.
    Busca dos cosas: 'Cajas que se rompen' (Block Break) y 'Velas gemelas' (Double Doji).
    """

    def __init__(self, data: pd.DataFrame):
        # Cuando nace el analista, le damos los datos del pasado.
        # Data tiene que tener: precio de apertura, alto, bajo, cierre y volumen.
        self.df = data
        # Nada más empezar, calculamos las líneas guía.
        self._calcular_indicadores()

    def _calcular_indicadores(self):
        # Calculamos la EMA 20 (La línea sagrada).
        # Es el promedio de los últimos 20 precios, pero dando más importancia a los nuevos.
        self.df['EMA_20'] = ta.ema(self.df['close'], length=20)
        
        # Calculamos el ATR (El medidor de nerviosismo).
        # Nos dice cuánto se mueve el precio normalmente arriba y abajo.
        self.df['ATR'] = ta.atr(self.df['high'], self.df['low'], self.df['close'], length=14)

    def detectar_block_break(self) -> dict:
        """
        BUSCA EL PATRÓN: BLOCK BREAK (La Caja Explosiva).
        Es cuando el precio se queda quieto en una cajita y de repente salta.
        """
        # Si tenemos poquitos datos (menos de 25 velas), no podemos mirar nada.
        if len(self.df) < 25: 
            return {"senal": False}

        # Cogemos las últimas 7 velas para mirarlas con lupa.
        last_candles = self.df.tail(7) 
        
        # Miramos el precio de AHORA MISMO (la última vela).
        current_price = last_candles['close'].iloc[-1]
        
        # Miramos dónde está la línea sagrada (EMA 20) ahora mismo.
        ema_20 = last_candles['EMA_20'].iloc[-1]

        # 1. Definimos la Caja (El Bloque).
        # Miramos las velas anteriores (todas menos la última que se está moviendo).
        block = last_candles.iloc[:-1] 
        
        # Buscamos el punto más alto del techo de la caja.
        block_high = block['high'].max()
        # Buscamos el punto más bajo del suelo de la caja.
        block_low = block['low'].min()
        # Calculamos la altura de la caja (Techo - Suelo).
        block_height = block_high - block_low
        
        # Miramos cuánto se suele mover el precio (ATR) hace dos velas.
        atr_promedio = self.df['ATR'].iloc[-2]
        
        # REGLA: La caja tiene que ser pequeña (comprimida).
        # Si la altura es menor que 1.5 veces lo normal, es una caja apretada.
        es_comprimido = block_height < (atr_promedio * 1.5)

        # 2. REGLA: La caja tiene que estar pegada a la línea sagrada (EMA 20).
        # Calculamos la distancia entre el centro de la caja y la línea.
        distancia_ema = abs(block['close'].mean() - ema_20)
        # Tiene que estar muy cerca (menos de la mitad de un movimiento normal).
        es_cercano_ema = distancia_ema < (atr_promedio * 0.5)

        # 3. REGLA: El salto (Ruptura).
        # El precio de ahora tiene que haber roto el techo de la caja.
        es_ruptura = current_price > block_high

        # Si se cumplen las tres reglas a la vez...
        if es_comprimido and es_cercano_ema and es_ruptura:
            # ... ¡TENEMOS SEÑAL!
            return {
                "senal": True, 
                "tipo": "VOLMAN_BB_BULL", # Nombre clave del movimiento.
                "entrada": current_price, # Precio al que disparamos.
                "stop_loss": block_low,   # Si el precio baja al suelo de la caja, huimos.
                "confianza": 0.9          # Estamos muy seguros (90%).
            }
        
        # Si no se cumple, no hacemos nada.
        return {"senal": False}

    def detectar_double_doji(self) -> dict:
        """
        BUSCA EL PATRÓN: DOUBLE DOJI (Las Gemelas Indecisas).
        Es cuando el precio para a descansar sobre la línea y luego sigue subiendo.
        """
        # Necesitamos al menos 5 velas para ver esto.
        if len(self.df) < 5: 
            return {"senal": False}

        # Miramos las dos velas anteriores a la de ahora.
        c1 = self.df.iloc[-2] # La penúltima.
        c2 = self.df.iloc[-3] # La antepenúltima.
        current = self.df.iloc[-1] # La de ahora.

        # REGLA: ¿Son Dojis? (Cuerpo muy pequeñito, casi una línea).
        # Si la diferencia entre abrir y cerrar es minúscula comparada con la mecha.
        es_doji_1 = abs(c1['open'] - c1['close']) <= (c1['high'] - c1['low']) * 0.15
        es_doji_2 = abs(c2['open'] - c2['close']) <= (c2['high'] - c2['low']) * 0.15

        # REGLA: ¿Están tocando la línea sagrada (EMA 20)?
        # El precio bajo debe ser menor que la línea, y el alto mayor. (La cruzan).
        toca_ema = (c1['low'] <= c1['EMA_20'] <= c1['high']) or 
                   (c2['low'] <= c2['EMA_20'] <= c2['high'])

        # REGLA: El salto (Ruptura).
        # El precio de ahora tiene que superar el punto más alto de las gemelas.
        max_dojis = max(c1['high'], c2['high'])
        ruptura = current['close'] > max_dojis

        # Si son gemelas, tocan la línea y el precio salta...
        if es_doji_1 and es_doji_2 and toca_ema and ruptura:
            # ... ¡TENEMOS SEÑAL!
            return {
                "senal": True,
                "tipo": "VOLMAN_DD_SCALP", # Nombre clave.
                "entrada": current['close'], # Precio de disparo.
                "stop_loss": min(c1['low'], c2['low']), # Si baja de los pies de las gemelas, huimos.
                "confianza": 0.85 # Estamos bastante seguros (85%).
            }

        # Si no, nada.
        return {"senal": False}
