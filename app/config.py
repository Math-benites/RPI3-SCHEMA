import storage

# Carrega valores do armazenamento
credit = storage.load_int("credit", 0)
salescounter = storage.load_int("salescounter", 0)
temperature = storage.load_float("temperature", 0.0)  # Adicionando a temperatura com valor padrão 0.0
start_routine = False
is_routine_running = False
