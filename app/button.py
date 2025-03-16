from gpiozero import Button
import time
import config
import storage
import logger

CREDIT_BUTTON_PIN = 17
START_BUTTON_PIN = 27

credit_button = Button(CREDIT_BUTTON_PIN, pull_up=True)
start_button = Button(START_BUTTON_PIN, pull_up=True)

def log(msg):
    """Função para imprimir logs com timestamp."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def button_task():
    while True:
        if credit_button.is_pressed:
            config.credit += 1
            logger.log_message(f"Crédito Adicionado: {config.credit}")
            storage.save_int("credit", config.credit)
            time.sleep(1)

        if start_button.is_pressed and not config.is_routine_running and config.credit > 0:
            config.credit -= 1
            config.start_routine = True
            storage.save_int("credit", config.credit)
            config.salescounter += 1
            storage.save_int("salescounter", config.salescounter)
            logger.log_message(f"Vendas realizadas: {config.salescounter}")
            time.sleep(1)
