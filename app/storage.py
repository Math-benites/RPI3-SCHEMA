import json
import os

# Caminho do arquivo onde os dados serão armazenados
STORAGE_FILE = "storage.json"

# Função para carregar dados do arquivo
def load_data():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as file:
            return json.load(file)
    return {}

# Função para salvar os dados no arquivo
def save_data(data):
    with open(STORAGE_FILE, "w") as file:
        json.dump(data, file)

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
