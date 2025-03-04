import time
import config
import storage
import digitalio
from mcp import mcp  # Importa o MCP23017 já inicializado
import logger

# Definição dos pinos no MCP23017
credit_button = mcp.get_pin(8)   # Pino B0
start_button = mcp.get_pin(9)    # Pino B1

# Configura os pinos como entrada com pull-up
credit_button.direction = digitalio.Direction.INPUT
credit_button.pull = digitalio.Pull.UP

start_button.direction = digitalio.Direction.INPUT
start_button.pull = digitalio.Pull.UP

def log(msg):
    """Função para imprimir logs com timestamp."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def button_task():
    debounce_delay = 1  # 1 segundo para evitar múltiplos cliques rápidos
    last_credit_press = 0
    last_start_press = 0

    while True:
        current_time = time.time()

        # Botão de crédito
        if not credit_button.value:  # Botão pressionado (LOW)
            if current_time - last_credit_press > debounce_delay:
                config.credit += 1
                logger.log_message(f"Crédito Adicionado: {config.credit}")
                storage.save_int("credit", config.credit)
                last_credit_press = current_time

        # Botão de start
        if not start_button.value:  # Botão pressionado (LOW)
            if current_time - last_start_press > debounce_delay and not config.is_routine_running:
                if config.credit > 0:
                    config.credit -= 1
                    config.start_routine = True
                    storage.save_int("credit", config.credit)
                    config.salescounter += 1
                    storage.save_int("salescounter", config.salescounter)
                    logger.log_message(f"Vendas realizadas: {config.salescounter}")
                last_start_press = current_time

        time.sleep(0.1)  # Pequeno delay para evitar uso excessivo da CPU
