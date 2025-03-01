import paho.mqtt.client as mqtt
import json
import time
import storage  # Arquivo de gerenciamento de armazenamento
import config  # Arquivo de configuração que contém o valor do hardware
import threading

# Definindo o servidor, porta e tópico MQTT
mqtt_server = "mqtt.eclipseprojects.io"  # Substitua pelo seu servidor MQTT
mqtt_port = 1883
mqtt_topic = "express/{}/publish".format(config.hardware)  # Tópico para enviar os dados

# Função para obter os dados de storage.json
def get_storage_data():
    return storage.load_data()

# Função chamada quando o cliente MQTT se conecta
def on_connect(client, userdata, flags, rc):
    print(f"Conectado com o código: {rc}")
    # Após a conexão, o cliente pode iniciar o envio de dados ou subscrever tópicos
    # Aqui, estamos apenas publicando os dados

    # Enviar os dados do storage.json para o servidor MQTT
    data = get_storage_data()  # Obtém os dados de storage.json
    if data:
        client.publish(mqtt_topic, json.dumps(data))
        print(f"Enviado dados para o tópico {mqtt_topic}: {data}")

# Função para enviar dados via MQTT
def send_mqtt_data():
    client = mqtt.Client()  # Cria uma nova instância do cliente MQTT
    client.on_connect = on_connect  # Define a função de callback para a conexão

    # Conectar ao servidor MQTT
    client.connect(mqtt_server, mqtt_port, 60)

    # Inicia o loop de comunicação do cliente
    client.loop_start()

    try:
        while True:
            # A cada 15 segundos, os dados são enviados para o servidor MQTT
            data = get_storage_data()  # Obtém os dados de storage.json
            if data:
                # Publica os dados no tópico MQTT
                client.publish(mqtt_topic, json.dumps(data))
                print(f"Enviado dados: {data}")
            time.sleep(15)  # Atraso de 15 segundos entre as publicações
    except KeyboardInterrupt:
        print("Processo interrompido")

if __name__ == "__main__":
    # Cria e inicia a thread para enviar dados via MQTT
    mqtt_thread = threading.Thread(target=send_mqtt_data, daemon=True)
    mqtt_thread.start()

    try:
        while True:
            pass  # Mantém o programa rodando enquanto as threads continuam
    except KeyboardInterrupt:
        print("Programa encerrado.")
