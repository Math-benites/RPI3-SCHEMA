import json
import os

# Caminho do arquivo onde os dados serão armazenados
STORAGE_FILE = "storage.json"

# Função para carregar dados do arquivo
def load_data():
    if not os.path.exists(STORAGE_FILE):
        return {}

    try:
        with open(STORAGE_FILE, "r") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, ValueError):
        print("Erro ao carregar storage.json. O arquivo pode estar corrompido. Resetando...")
        return {}

# Função para salvar os dados no arquivo de forma segura
def save_data(data):
    temp_file = STORAGE_FILE + ".tmp"

    try:
        with open(temp_file, "w") as file:
            json.dump(data, file, indent=4)
        os.replace(temp_file, STORAGE_FILE)  # Substitui o original somente se a gravação foi bem-sucedida
    except Exception as e:
        print(f"Erro ao salvar o arquivo JSON: {e}")

# Função para carregar um valor inteiro
def load_int(key, default=0):
    data = load_data()
    return data.get(key, default)

# Função para carregar um valor de ponto flutuante
def load_float(key, default=0.0):
    data = load_data()
    return data.get(key, default)

# Função para salvar um valor inteiro
def save_int(key, value):
    data = load_data()
    data[key] = value
    save_data(data)

# Função para salvar um valor de ponto flutuante
def save_float(key, value):
    data = load_data()
    data[key] = value
    save_data(data)
