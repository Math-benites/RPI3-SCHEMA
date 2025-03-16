import time
from gpiozero import LED, OutputDevice
import config
import storage
import logger

# Definição dos pinos GPIO para os LEDs e relés
R0_PIN = 19  # LED READY
R1_PIN = 16  # LED RUNNING
R2_PIN = 26  # LED VAZIO
R3_PIN = 20  # RELE MOTOR
R4_PIN = 21  # RELE TAMPA

# Configuração dos LEDs e relés
led_ready = LED(R0_PIN)
led_running = LED(R1_PIN)
led_vazio = LED(R2_PIN)
rele_motor = OutputDevice(R3_PIN)
rele_tampa = OutputDevice(R4_PIN)

def log(msg):
    """Função para imprimir logs com timestamp."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def routine_task():
    """Gerencia a rotina principal."""
    while True:
        # Se houver crédito, acende o LED READY
        if config.credit > 0:
            led_ready.on()
        else:
            led_ready.off()

        # Se a rotina for iniciada
        if config.start_routine:
            config.start_routine = False
            config.is_routine_running = True

            # Acende o LED RUNNING
            led_running.on()
            logger.log_message("Routine -> START")
            
            # Aciona o relé do motor
            rele_motor.on()
            time.sleep(3)  # Aguarda 3 segundos
            
            # Aciona o relé da tampa
            rele_tampa.on()
            time.sleep(3)  # Aguarda 3 segundos

            # Desliga os LEDs e relés
            led_running.off()
            rele_motor.off()
            rele_tampa.off()
            logger.log_message("Routine -> END")

            config.is_routine_running = False

        time.sleep(0.1)  # Delay para não sobrecarregar a CPU
