import threading
import gpio_thread

def main():
    # Cria e inicia a thread para a tarefa gpio_task
    gpio_thread_1 = threading.Thread(target=gpio_thread.gpio_task)
    gpio_thread_1.daemon = True
    gpio_thread_1.start()

    # Adiciona outras threads ou funções conforme necessário
    while True:
        # Aqui você pode adicionar outras funções ou interações no seu loop principal
        pass

if __name__ == "__main__":
    main()
