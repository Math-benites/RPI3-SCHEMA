import storage
import os
import time

# Carrega valores do armazenamento
credit = storage.load_int("credit", 0)
salescounter = storage.load_int("salescounter", 0)
temperature = storage.load_float("temperature", 0.0)  # Adicionando a temperatura com valor padrão 0.0
start_routine = False
is_routine_running = False

# Definindo o hardware (valor fixo ou ID único do dispositivo)
hardware = 340656  # Altere conforme necessário (exemplo: número do dispositivo ou ID)
