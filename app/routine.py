import time
import config
import storage
from mcp import mcp  # Importa o MCP23017 já inicializado
import digitalio

# Definição dos pinos do MCP23017
R0 = mcp.get_pin(0)   # Pino A0 no MCP23017 (LED READY)
R1 = mcp.get_pin(1)   # Pino A1 no MCP23017 (LED RUNNING)
R2 = mcp.get_pin(2)   # Pino A0 no MCP23017 (LED READY)
R3 = mcp.get_pin(3)   # Pino A1 no MCP23017 (LED RUNNING)

# Configura os pinos como saída
R0.direction = digitalio.Direction.OUTPUT
R1.direction = digitalio.Direction.OUTPUT
R2.direction = digitalio.Direction.OUTPUT
R3.direction = digitalio.Direction.OUTPUT

def routine_task():
    """Gerencia a rotina principal."""
    while True:
        # Se houver crédito, acende o LED READY
        if config.credit > 0:
            R0.value = True
        else:
            R0.value = False

        # Se a rotina for iniciada
        if config.start_routine:
            config.start_routine = False
            config.is_routine_running = True

            # Acende o LED RUNNING 
            R1.value = True
            print("R1 LED -> 1")
            # Acende o MOTOR  
            R2.value = True
            print("R2 MOTOR -> 1")
            time.sleep(3)  # Aguarda 6 segundos
            R3.value = True
            print("R3 TAMPA -> 1")
            time.sleep(3)  # Aguarda 6 segundos

            # Desliga o LED RUNNING
            R1.value = False
            R2.value = False
            R3.value = False
            print("R1 -> 0")
            print("R2 -> 0")
            print("R3 -> 0")

            config.is_routine_running = False

        time.sleep(0.1)  # Delay para não sobrecarregar a CPU
