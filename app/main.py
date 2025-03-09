import threading
import button
import routine
import ds18b20
import init
import mqtt
import logger
import lcd
import ngelo

def start_thread(target, name):
    """Função para iniciar uma thread e reiniciar em caso de falha."""
    while True:
        try:
            thread = threading.Thread(target=target, daemon=True, name=name)
            thread.start()
            thread.join()  # A thread irá rodar até terminar. Em caso de erro, o código abaixo será executado.
        except Exception as e:
            logger.log_message(f"Erro na thread {name}: {e}. Tentando reiniciar a thread.")
            continue  # Em caso de erro, reinicia a thread

def main():
    # Cria e inicia a thread para inicializar o hardware e uptime
    threading.Thread(target=start_thread, args=(init.main, 'init_thread'), daemon=True).start()

    # Cria e inicia a thread para gerenciar os botões
    threading.Thread(target=start_thread, args=(button.button_task, 'button_thread'), daemon=True).start()

    # Inicia a rotina em uma thread separada
    threading.Thread(target=start_thread, args=(routine.routine_task, 'routine_thread'), daemon=True).start()

    # Certifique-se de que a função 'monitor_temperature' esteja sendo chamada corretamente
    threading.Thread(target=start_thread, args=(ds18b20.monitor_temperature, 'temp_thread'), daemon=True).start()

    # Cria e inicia a thread para enviar dados via MQTT
    threading.Thread(target=start_thread, args=(mqtt.send_mqtt_data, 'mqtt_thread'), daemon=True).start()

    # Cria e inicia a thread nivel gelo
    threading.Thread(target=start_thread, args=(lcd.update_display, 'lcd_thread'), daemon=True).start()

    threading.Thread(target=start_thread, args=(ngelo.ngelo_task, 'gelo_thread'), daemon=True).start()


    try:
        while True:
            pass  # Mantém o programa rodando
    except KeyboardInterrupt:
        logger.log_message("Interrompido programa")

if __name__ == "__main__":
    main()
