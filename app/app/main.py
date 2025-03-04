import threading
import button
import routine
import ds18b20  # Este import é para seu módulo DS18B20
import init  # Importando o módulo init para inicializar hardware e uptime
import mqtt  # Importando o módulo MQTT para enviar dados
import logger

def main():
    # Cria e inicia a thread para inicializar o hardware e uptime
    init_thread = threading.Thread(target=init.main, daemon=True)
    init_thread.start()

    # Cria e inicia a thread para gerenciar os botões
    button_thread = threading.Thread(target=button.button_task, daemon=True)
    button_thread.start()

    # Inicia a rotina em uma thread separada
    routine_thread = threading.Thread(target=routine.routine_task, daemon=True)
    routine_thread.start()

    # Certifique-se de que a função 'monitor_temperature' esteja sendo chamada corretamente
    temp_thread = threading.Thread(target=ds18b20.monitor_temperature, daemon=True)
    temp_thread.start()

    # Cria e inicia a thread para enviar dados via MQTT
    mqtt_thread = threading.Thread(target=mqtt.send_mqtt_data, daemon=True)
    mqtt_thread.start()

    try:
        while True:
            pass  # Mantém o programa rodando
    except KeyboardInterrupt:
        logger.log_message("Interrompido programa")

if __name__ == "__main__":
    main()
