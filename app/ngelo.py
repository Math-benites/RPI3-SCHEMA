from mcp import mcp  # Importa o MCP23017 já inicializado
import digitalio
import logger
import storage
import config
from time import sleep

# Definição dos pinos no MCP23017
N1 = mcp.get_pin(10)   # Pino B3 (Nível 1)
N2 = mcp.get_pin(11)   # Pino B4 (Nível 2)
N3 = mcp.get_pin(12)   # Pino B5 (Nível 3)

# Configura os pinos como entrada com pull-up
N1.direction = digitalio.Direction.INPUT
N1.pull = digitalio.Pull.UP

N2.direction = digitalio.Direction.INPUT
N2.pull = digitalio.Pull.UP

N3.direction = digitalio.Direction.INPUT
N3.pull = digitalio.Pull.UP

def ngelo_task():
    nivel_gelo = 0  # Valor inicial

    while True:
        # Verifica o estado dos sensores para determinar o nível de gelo
        if not N3.value:  # Nível 3 fechado (gelo alto)
            nivel_gelo = 3
            logger.log_message("Gelo no Nível 3 (Alto)", level="info")
        elif not N2.value:  # Nível 2 fechado (gelo médio)
            nivel_gelo = 2
            logger.log_message("Gelo no Nível 2 (Médio)", level="info")
        elif not N1.value:  # Nível 1 fechado (gelo baixo)
            nivel_gelo = 1
            logger.log_message("Gelo no Nível 1 (Baixo)", level="info")
        else:  # Se todos os sensores estiverem abertos
            nivel_gelo = 0
            logger.log_message("Gelo: Vazio", level="info")

        # Salva o valor do nível de gelo no storage
        storage.save_int("gelo", nivel_gelo)

        sleep(15.0)  # Delay para não sobrecarregar a CPU

