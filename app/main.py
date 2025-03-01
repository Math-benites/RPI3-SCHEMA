import threading
import button
import routine
import ds18b20  # Este import é para seu módulo DS18B20

def main():
    # Cria e inicia a thread para gerenciar os botões
    button_thread = threading.Thread(target=button.button_task, daemon=True)
    button_thread.start()

    # Inicia a rotina em uma thread separada
    routine_thread = threading.Thread(target=routine.routine_task, daemon=True)
    routine_thread.start()

    # Inicia o monitoramento da temperatura em uma thread separada
    # Certifique-se de que a função 'monitor_temperature' esteja sendo chamada corretamente
    temp_thread = threading.Thread(target=ds18b20.monitor_temperature, daemon=True)
    temp_thread.start()

    try:
        while True:
            pass  # Mantém o programa rodando
    except KeyboardInterrupt:
        print("Programa encerrado.")

if __name__ == "__main__":
    main()
