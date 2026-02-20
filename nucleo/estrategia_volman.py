# nucleo/estrategia_volman.py
# 🏎️ ESTRATEGIA DE CARRERAS (VOLMAN VECTORIZADO)
# Este archivo es el mismo detective de antes, pero ahora mira 10 años de gráficos en 1 segundo.
# Usamos "Magia de Tablas" (Vectorización) en lugar de mirar vela por vela.

import pandas as pd  # La tabla mágica.
import pandas_ta as ta  # Las herramientas de dibujo (indicadores).
import numpy as np  # Matemáticas rápidas.

class AnalistaVolmanVectorizado:
    """
    El cerebro ultra-rápido de Bob Volman.
    Calcula todo de golpe para que el Laboratorio pueda hacer miles de pruebas.
    """

    def __init__(self):
        # Configuración básica (Parámetros que podemos cambiar).
        self.periodo_ema = 20  # La media móvil de 20 velas.
        self.periodo_atr = 14  # Para medir volatilidad.
        self.bloque_velas = 7  # Cuántas velas miramos para la "Caja Explosiva".

    def populate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula las líneas y números importantes de TODA la historia a la vez.
        """
        # 1. EMA 20 (La línea sagrada).
        # Usamos pandas_ta para calcular la columna entera.
        df['EMA_20'] = ta.ema(df['close'], length=self.periodo_ema)

        # 2. ATR (El medidor de nerviosismo).
        df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=self.periodo_atr)

        # 3. Canales de Donchian (Para ver máximos y mínimos del bloque).
        # Esto nos dice cuál fue el precio más alto y más bajo de las últimas 7 velas.
        # Shift(1) es importante: queremos el máximo de las 7 ANTERIORES, sin contar la actual.
        df['donchian_high'] = df['high'].rolling(window=self.bloque_velas).max().shift(1)
        df['donchian_low'] = df['low'].rolling(window=self.bloque_velas).min().shift(1)

        # 4. Altura del Bloque (Tamaño de la caja).
        df['block_height'] = df['donchian_high'] - df['donchian_low']

        # 5. Distancia a la EMA (Qué tan lejos estamos de la línea sagrada).
        # Usamos el precio medio del bloque (promedio de alto y bajo) comparado con la EMA.
        df['block_center'] = (df['donchian_high'] + df['donchian_low']) / 2
        df['dist_ema'] = abs(df['block_center'] - df['EMA_20'])

        # 6. Definición de Doji (Para el patrón de Gemelas).
        # Un Doji es cuando el cuerpo es muy pequeño comparado con la mecha total.
        cuerpo = abs(df['open'] - df['close'])
        mecha_total = df['high'] - df['low']
        # Si el cuerpo es menor al 15% de la mecha, es un Doji (True/False).
        # Evitamos dividir por cero con np.where.
        df['is_doji'] = np.where(mecha_total > 0, cuerpo <= (mecha_total * 0.15), False)

        return df

    def populate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Busca las señales de COMPRA y VENTA en toda la tabla a la vez.
        Crea columnas 'enter_long' y 'exit_long' con 1 (Sí) o 0 (No).
        """
        # Aseguramos que tenemos los indicadores calculados.
        if 'EMA_20' not in df.columns:
            df = self.populate_indicators(df)

        # --- PATRÓN 1: BLOCK BREAK (La Caja Explosiva) ---
        
        # Regla 1: Caja pequeña (Comprimida). Altura < 1.5 veces el ATR promedio.
        # Shift(1) porque miramos el ATR de ayer.
        atr_ayer = df['ATR'].shift(1)
        es_comprimido = df['block_height'] < (atr_ayer * 1.5)

        # Regla 2: Pegado a la EMA. Distancia < 0.5 veces el ATR.
        es_cercano_ema = df['dist_ema'] < (atr_ayer * 0.5)

        # Regla 3: Ruptura (El precio actual rompe el techo de la caja).
        es_ruptura = df['close'] > df['donchian_high']

        # Combinamos todo: Si (Comprimido Y Cercano Y Ruptura) -> SEÑAL BB.
        senal_bb = es_comprimido & es_cercano_ema & es_ruptura

        # --- PATRÓN 2: DOUBLE DOJI (Las Gemelas) ---
        
        # Miramos si la vela de ayer (shift 1) y la de antes de ayer (shift 2) eran Dojis.
        doji_ayer = df['is_doji'].shift(1)
        doji_anteayer = df['is_doji'].shift(2)

        # Miramos si las Gemelas tocaban la EMA 20.
        # (El mínimo era menor que la EMA y el máximo mayor que la EMA).
        toca_ema_ayer = (df['low'].shift(1) <= df['EMA_20'].shift(1)) & (df['high'].shift(1) >= df['EMA_20'].shift(1))
        toca_ema_anteayer = (df['low'].shift(2) <= df['EMA_20'].shift(2)) & (df['high'].shift(2) >= df['EMA_20'].shift(2))
        
        tocan_ema = toca_ema_ayer | toca_ema_anteayer # Con que una toque vale.

        # Ruptura de Dojis: El precio actual supera el máximo de las dos gemelas.
        max_dojis = df[['high']].shift(1).rolling(2).max()['high'] # Máximo de las 2 anteriores.
        ruptura_doji = df['close'] > max_dojis

        # Combinamos: Si (Doji Ayer Y Doji Anteayer Y Tocan EMA Y Ruptura) -> SEÑAL DD.
        senal_dd = doji_ayer & doji_anteayer & tocan_ema & ruptura_doji

        # --- SEÑAL FINAL ---
        # Compramos si se cumple CUALQUIERA de los dos patrones.
        # Ponemos un 1 donde sea True, y un 0 donde sea False.
        df['enter_long'] = (senal_bb | senal_dd).astype(int)

        # --- SALIDAS (STOP LOSS Y TAKE PROFIT VECTORIZADO) ---
        # Esto es simple para el vectorizado:
        # Salimos si el precio cruza la EMA hacia abajo (cierre < EMA).
        # (En backtesting real usaremos stop loss fijo, pero esto marca tendencia).
        df['exit_long'] = (df['close'] < df['EMA_20']).astype(int)

        return df
