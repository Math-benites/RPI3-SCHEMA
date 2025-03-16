import storage
import time

# Caminho para o sensor DS18B20
sensor_path = "/sys/bus/w1/devices/28-125ad446ac08/w1_slave"  # Atualize com o seu ID de sensor

def read_temperature():
    try:
        with open(sensor_path, 'r') as f:
            lines = f.readlines()
            if lines and lines[0].strip()[-3:] == 'YES':
                # Extrai e converte a temperatura para Celsius
                temp_data = lines[1].split('t=')[1]
                temperature = float(temp_data) / 1000  # Converte para Celsius
                return temperature
            else:
                print("Erro na leitura do sensor")
                return None
    except FileNotFoundError:
        print("Sensor não encontrado")
        return None

def monitor_temperature():
    while True:
        temperature = read_temperature()
        if temperature is not None:
            # Salva a temperatura no armazenamento
            storage.save_float("temperature", temperature)  # Salva a temperatura
        time.sleep(5)  # Atraso de 2 segundos entre leituras

# Função para iniciar a monitorização da temperatura em uma thread
def start_temperature_task():
    import threading
    temperature_thread = threading.Thread(target=monitor_temperature)
    temperature_thread.daemon = True  # Torna a thread uma daemon para que se finalize com o programa
    temperature_thread.start()

# Chamada para iniciar a tarefa de monitoramento
if __name__ == "__main__":
    start_temperature_task()
    while True:
        time.sleep(1)  # Mantém o loop principal rodando enquanto a thread de temperatura trabalha
