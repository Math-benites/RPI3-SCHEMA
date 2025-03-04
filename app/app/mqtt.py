import paho.mqtt.client as mqtt
import json
import time
import storage  # Gerenciamento de armazenamento
import config  # Configuração contendo hardware ID
import threading
import ds18b20
import init
import logger  # Importa o módulo de logging


# Configurações MQTT
MQTT_SERVER = "mqtt.eclipseprojects.io"
MQTT_PORT = 1883
MQTT_TOPIC = f"express/{config.hardware}/publish"

# Inicializa o cliente MQTT
mqtt_client = mqtt.Client()

def log(msg):
    """Função para imprimir logs com timestamp."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def on_connect(client, userdata, flags, rc):
    """Callback chamada ao conectar no MQTT."""
    if rc == 0:
        logger.log_message("✅ Conectado ao MQTT com sucesso!")
    else:
        logger.log_message(f"⚠️ Falha na conexão MQTT. Código de retorno: {rc}")

def send_mqtt_data():
    """Envia dados via MQTT periodicamente."""
    mqtt_client.on_connect = on_connect

    try:
        logger.log_message("🔌 Conectando ao servidor MQTT...")
        logger.log_message(f"Server: {MQTT_SERVER}")
        logger.log_message(f"Port: {MQTT_PORT}")
        logger.log_message(f"Topic: {MQTT_TOPIC}")
        mqtt_client.connect(MQTT_SERVER, MQTT_PORT, 60)
        mqtt_client.loop_start()

        while True:
            temperature = ds18b20.read_temperature()
            hardware = storage.load_int("hardware")
            credit = storage.load_int("credit", 0)
            salescounter = storage.load_int("salescounter", 0)
            uptime = init.get_uptime()

            # Tratamento para evitar valores None
            if temperature is None:
                log("⚠️ Erro ao ler a temperatura, ignorando envio.")
                temperature = 0.0  # Define um valor padrão

            if uptime is None:
                log("⚠️ Erro ao obter uptime, definindo como 0.")
                uptime = 0.0  # Define um valor padrão

            payload = {
                "temperature": round(temperature, 3),
                "hardware": hardware,
                "uptime": round(uptime, 2),
                "credit": credit,
                "salescounter": salescounter
            }

            mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
            logger.log_message(f"📤 Enviado dados: {payload}")

            time.sleep(10)

    except Exception as e:
        logger.log_message(f"❌ Erro no envio MQTT: {e}")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    mqtt_thread = threading.Thread(target=send_mqtt_data, daemon=True)
    mqtt_thread.start()

    try:
        while True:
            time.sleep(1)  # Mantém o programa ativo
    except KeyboardInterrupt:
        log("⏹️ Programa encerrado.")
