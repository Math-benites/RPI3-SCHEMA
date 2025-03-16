from gpiozero import Button  # Importa a classe Button do gpiozero
import logger
import storage
import config
from time import sleep
import routine

# Definição dos pinos GPIO para os níveis de gelo
N1_PIN = 22  # Defina os pinos físicos do Raspberry Pi (exemplo: GPIO 22)
N2_PIN = 23  # GPIO 23
N3_PIN = 24  # GPIO 24

# Configuração dos botões para os pinos de entrada
N1 = Button(N1_PIN, pull_up=True)  # Configura N1 com pull-up
N2 = Button(N2_PIN, pull_up=True)  # Configura N2 com pull-up
N3 = Button(N3_PIN, pull_up=True)  # Configura N3 com pull-up

def ngelo_task():
    nivel_gelo = 0  # Valor inicial

    while True:        
        # Verifica o estado dos sensores para determinar o nível de gelo
        if N3.is_pressed:  # Nível 3 fechado (gelo alto)
            nivel_gelo = 3
            logger.log_message("Gelo no Nível 3 (Alto)", level="info")
            routine.rele_motor.off()
        elif N2.is_pressed:  # Nível 2 fechado (gelo médio)
            nivel_gelo = 2
            logger.log_message("Gelo no Nível 2 (Médio)", level="info")
            routine.rele_motor.off()
        elif N1.is_pressed:  # Nível 1 fechado (gelo baixo)
            nivel_gelo = 1
            logger.log_message("Gelo no Nível 1 (Baixo)", level="info")
            routine.rele_motor.off()
        else:  # Se todos os sensores estiverem abertos
            nivel_gelo = 0
            logger.log_message("Gelo: Vazio", level="info")
            routine.rele_motor.on()


        # Salva o valor do nível de gelo no storage
        storage.save_int("gelo", nivel_gelo)

        sleep(15.0)  # Delay para não sobrecarregar a CPU


