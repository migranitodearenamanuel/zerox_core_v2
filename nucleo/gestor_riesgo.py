# nucleo/gestor_riesgo.py
# 📉 EL MOTOR DE MATEMÁTICAS (GESTOR DE RIESGO ADAPTATIVO)
# Este archivo decide cuánto apostar según cuánto dinero tenemos.

import math  # Traemos las matemáticas.

class QuantEngine:
    def __init__(self, capital_inicial: float = 15.0):
        # Arrancamos con nuestro dinero actual.
        self.capital = capital_inicial

    def calcular_kelly_adaptativo(self, prob_win: float = 0.6, ratio_win_loss: float = 2.0) -> float:
        """
        Calcula la apuesta usando el Criterio de Kelly Adaptativo.
        Cambia la agresividad según en qué "Fase de Riqueza" estemos.
        """
        # 1. Definimos la Fase según el capital.
        if self.capital < 1000:
            # FASE 1: POBREZA (Salir del hoyo).
            # Arriesgamos más para crecer rápido.
            factor_kelly = 0.5 # Medio Kelly (Agresivo pero no suicida).
            fase = "CRECIMIENTO_AGRESIVO"
            
        elif self.capital < 100000:
            # FASE 2: CLASE MEDIA (Consolidar).
            # Bajamos un poco el riesgo.
            factor_kelly = 0.3
            fase = "CRECIMIENTO_MODERADO"
            
        else:
            # FASE 3: RICOS (Preservar fortuna).
            # Arriesgamos muy poco porque ya tenemos mucho.
            factor_kelly = 0.1
            fase = "INSTITUCIONAL_PRESERVACION"

        # 2. Calculamos Kelly Puro.
        # Fórmula: (Probabilidad Ganar * Ratio - Probabilidad Perder) / Ratio
        prob_loss = 1.0 - prob_win
        kelly_puro = (prob_win * ratio_win_loss - prob_loss) / ratio_win_loss

        # Si la esperanza es negativa, no operamos.
        if kelly_puro <= 0:
            return 0.0

        # 3. Ajustamos por la Fase (Kelly Fraccional).
        fraccion_apuesta = kelly_puro * factor_kelly
        
        # 4. Límite de seguridad absoluto (Nunca apostar más del 20% de la cuenta).
        fraccion_segura = min(fraccion_apuesta, 0.20)
        
        monto_apuesta = self.capital * fraccion_segura
        
        # (Opcional) Mostramos info si queremos depurar.
        # print(f"Gestor Riesgo: Fase {fase} | Kelly {factor_kelly} | Apuesta: {monto_apuesta:.2f}")

        return monto_apuesta

    def calcular_stop_loss_tecnico(self, precio_entrada: float, volatilidad_atr: float) -> float:
        """
        Calcula el Stop Loss basándose en la volatilidad (ATR), no en porcentajes fijos.
        """
        # Usamos 2 veces el ATR como margen de seguridad.
        distancia_stop = volatilidad_atr * 2.0
        precio_stop = precio_entrada - distancia_stop
        return precio_stop
