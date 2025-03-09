import lcd_lib
import time
import storage
import ds18b20
import mqtt

lcd = lcd_lib.lcd()

def update_display():
    while True:
        # Carrega a temperatura
        temperature = storage.load_float("temperature", 0.0)  # Adicionando a temperatura com valor padrão 0.0
        credit = storage.load_int("credit", 0)

        # Exibe a temperatura diretamente na segunda linha, sobrescrevendo o texto atual
        lcd.lcd_display_string(f"Credito: {credit}", 1, 1)
        lcd.lcd_display_string(f"{mqtt.mqtt_connected}",1,18)
        lcd.lcd_display_string(f"Temp: {temperature:.2f} C", 2, 1)
        lcd.lcd_display_string("Nivel Gelo : [99]",4,1)


        # A pausa de 2 segundos evita o uso excessivo de CPU
        time.sleep(0.1)

