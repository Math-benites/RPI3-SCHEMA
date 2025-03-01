import threading
import time
import json
import os
import storage  # Assume-se que storage é o arquivo que gerencia o arquivo storage.json
import config  # Importando o arquivo de configuração para acessar o hardware

# Função para obter o uptime do sistema
def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            return uptime_seconds
    except FileNotFoundError:
        print("Erro ao ler o uptime do sistema.")
        return 0.0

# Função para inicializar o sistema, definir o hardware e o uptime
def main():
    while True:
        # Usando o hardware do config.py
        hardware = config.hardware  # Agora vem do arquivo config.py

        # Obtendo o uptime do sistema
        uptime = get_uptime()

        # Carregar dados existentes do arquivo
        data = storage.load_data()

        # Atualiza ou adiciona o valor de hardware e uptime aos dados
        data["hardware"] = hardware
        data["uptime"] = uptime

        # Salvar os dados no arquivo
        storage.save_data(data)
        time.sleep(15.0)  # Pequeno delay para evitar uso excessivo da CPU
