import paho.mqtt.client as mqtt
import json
import time
import storage  # Gerenciamento de armazenamento
import config  # Configuração contendo hardware ID
import threading
import ds18b20
import init
import logger  # Importa o módulo de logging
import lcd
import ngelo


# Configurações MQTT
MQTT_SERVER = "mqtt.eclipseprojects.io"
MQTT_PORT = 1883
MQTT_TOPIC = f"express/{config.hardware}/publish"

# Inicializa o cliente MQTT
mqtt_client = mqtt.Client()

# Variável para armazenar o status da conexão
mqtt_connected = "!"

def log(msg):
    """Função para imprimir logs com timestamp."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def on_connect(client, userdata, flags, rc):
    """Callback chamada ao conectar no MQTT."""
    global mqtt_connected
    if rc == 0:
        logger.log_message("✅ Conectado ao MQTT com sucesso!")
        mqtt_connected = " "
    else:
        logger.log_message(f"⚠️ Falha na conexão MQTT. Código de retorno: {rc}")
        mqtt_connected = "!"

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
            try:
                temperature = ds18b20.read_temperature()
                hardware = storage.load_int("hardware")
                credit = storage.load_int("credit", 0)
                salescounter = storage.load_int("salescounter", 0)
                uptime = init.get_uptime()
                gelo = storage.load_int("gelo",0)

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
                    "salescounter": salescounter,
                    "gelo": gelo
                }

                mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
                logger.log_message(f"📤 Enviado dados: {payload}")

                time.sleep(10)  # Aguarda 10 segundos antes de enviar novamente

            except (OSError, ConnectionError) as e:
                # Erro de rede (desconexão ou falha ao enviar dados)
                logger.log_message(f"❌ Erro na rede: {e}. Tentando reconectar...")
                mqtt_connected = "!"
                # Tenta reconectar ao MQTT
                try:
                    mqtt_client.reconnect()
                    logger.log_message("🔌 Reconectado ao servidor MQTT.")
                except Exception as e:
                    logger.log_message(f"❌ Erro ao tentar reconectar: {e}")

                time.sleep(5)  # Aguarda 5 segundos antes de tentar novamente

    except Exception as e:
        logger.log_message(f"❌ Erro no envio MQTT: {e}")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    # Inicia a thread para o envio dos dados MQTT
    mqtt_thread = threading.Thread(target=send_mqtt_data, daemon=True)
    mqtt_thread.start()
    try:
        while True:
            time.sleep(1)  # Mantém o programa ativo
    except KeyboardInterrupt:
        log("⏹️ Programa encerrado.")
