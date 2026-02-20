# nucleo/supervisor_autonomo.py
# 🛡️ EL ESCUDO ANTI-HACKERS (SUPERVISOR DE CONTRATOS MEJORADO)
# Este archivo es el policía del robot.
# Se conecta a la cadena de bloques y busca trampas en los contratos antes de comprar.

from web3 import Web3  # Usamos la herramienta para hablar con la blockchain.
import os  # Para leer las variables de entorno.
from dotenv import load_dotenv  # Para cargar las claves secretas.

# Cargamos el archivo .env por si acaso.
load_dotenv()

class AuditorEVM:
    def __init__(self, rpc_url: str = None):
        """
        Preparamos al policía para trabajar.
        Si no le damos una dirección web, busca una por defecto.
        """
        # Intentamos usar la URL que nos pasan, o la del archivo secreto, o una pública de Base.
        self.rpc_url = rpc_url or os.getenv("BASE_RPC_URL", "https://mainnet.base.org")
        
        # Conectamos con la blockchain.
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        # Este es el "molde" mínimo de un token (ABI) para poder hablar con él.
        # Solo necesitamos saber preguntar el saldo (balanceOf), el total (totalSupply) y aprobar gasto (approve).
        self.erc20_abi = [
            {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"},
            {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
            {"constant": False, "inputs": [{"name": "_spender", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "approve", "outputs": [{"name": "", "type": "bool"}], "type": "function"}
        ]

    def _simular_transaccion(self, token_address: str, router_address: str) -> bool:
        """
        (PRIVADO) Intenta hacer una operación falsa (sin gastar dinero) para ver si falla.
        Si falla, es probable que sea un Honeypot (trampa).
        """
        try:
            # Convertimos las direcciones a formato seguro (Checksum).
            token = self.w3.to_checksum_address(token_address)
            router = self.w3.to_checksum_address(router_address)
            
            # Usamos una dirección muerta para probar como remitente.
            sender = self.w3.to_checksum_address("0x000000000000000000000000000000000000dead") 

            # Creamos el objeto contrato para interactuar.
            contract = self.w3.eth.contract(address=token, abi=self.erc20_abi)
            
            # PRUEBA DE FUEGO: Intentamos aprobar al router para gastar tokens.
            # Muchos Honeypots fallan aquí para que no puedas vender.
            # Usamos .call() para simular sin gastar gas real.
            cantidad_infinita = self.w3.to_wei(1000000, 'ether')
            
            # Si esto da error, saltará al bloque 'except'.
            contract.functions.approve(router, cantidad_infinita).call({'from': sender})
            
            # Si llegamos aquí sin errores, el contrato responde bien. ¡Es buena señal!
            return True
            
        except Exception as e:
            # Si da error, asumimos que es una trampa o está roto.
            print(f"⚠️ Error simulando transacción (Honeypot sospechoso): {e}")
            return False

    def _verificar_liquidez_quemada(self, token_address: str) -> bool:
        """
        (PRIVADO) Comprueba si el creador ha renunciado al contrato o quemado la liquidez.
        (Versión simplificada: solo comprueba si el contrato tiene código).
        """
        try:
            address = self.w3.to_checksum_address(token_address)
            codigo = self.w3.eth.get_code(address)
            
            # Si el código está vacío, es una estafa seguro (no existe).
            if codigo == b'' or codigo == b'0x':
                return False
                
            return True
        except:
            return False

    def auditar_token(self, token_address: str) -> dict:
        """
        MÉTODO PÚBLICO PRINCIPAL.
        Orquesta todas las comprobaciones de seguridad.
        Devuelve un informe completo.
        """
        # Preparamos el informe de auditoría.
        reporte = {
            "es_seguro": False, # Por defecto, decimos que NO es seguro.
            "motivo": "",      # Aquí explicamos por qué.
        }
        
        print(f"🛡️ Auditor: Iniciando escaneo de {token_address}...")

        # 1. Comprobamos conexión básica.
        if not self.w3.is_connected():
            reporte["motivo"] = "Sin conexión al nodo RPC"
            return reporte
            
        # 2. Validamos la dirección del contrato.
        if not self.w3.is_address(token_address):
            reporte["motivo"] = "Dirección de contrato inválida"
            return reporte

        # 3. Verificamos que el contrato existe (tiene código).
        if not self._verificar_liquidez_quemada(token_address):
             reporte["motivo"] = "Contrato fantasma (sin código)"
             return reporte

        # 4. SIMULACIÓN DE HONEYPOT (La prueba más importante).
        # Usamos el router de Uniswap V2 como ejemplo de destino seguro.
        router_seguro = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D" 
        
        es_simulacion_exitosa = self._simular_transaccion(token_address, router_seguro)
        
        if not es_simulacion_exitosa:
            reporte["motivo"] = "Fallo crítico en simulación de venta (Posible Honeypot)"
            return reporte

        # Si llegamos hasta aquí, ha pasado todas las pruebas básicas.
        reporte["es_seguro"] = True
        reporte["motivo"] = "Auditoría EVM superada: Código válido y simulación exitosa."
        
        return reporte
