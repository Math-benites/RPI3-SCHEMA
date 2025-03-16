import lcd_lib
import time
import storage
import ds18b20
import mqtt

lcd = lcd_lib.lcd()

def update_display():
    while True:
        # Carrega os valores armazenados
        temperature = storage.load_float("temperature", 0.0)  
        credit = storage.load_int("credit", 0)
        nivel_gelo = storage.load_int("gelo", 0)  # Carrega o nível de gelo

        # Mapeia o nível de gelo para os valores desejados
        gelo_display = {0: "00", 1: "10", 2: "50", 3: "99"}.get(nivel_gelo, "00")
        if nivel_gelo == 0:
            # Faz a mensagem piscar
            lcd.lcd_display_string("SEM GELO - EM FABR.", 3, 1)
            time.sleep(0.5)  # Espera meio segundo
            lcd.lcd_display_string("                   ", 1, 1)  # Apaga a linha 3
            lcd.lcd_display_string("                   ", 2, 1)  # Apaga a linha 3
            lcd.lcd_display_string("                   ", 3, 1)  # Apaga a linha 3
            
            lcd.lcd_display_string(f"Nivel Gelo : [{gelo_display}]", 4, 1)
            time.sleep(0.5)  # Espera meio segundo
        else:
            lcd.lcd_display_string(f"Credito: {credit}", 1, 1)
            lcd.lcd_display_string(f"{mqtt.mqtt_connected}", 1, 18)
            lcd.lcd_display_string(f"Temp: {temperature:.2f} C", 2, 1)
            lcd.lcd_display_string("                   ", 3, 1)  # Apaga a mensagem
            lcd.lcd_display_string(f"Nivel Gelo : [{gelo_display}]", 4, 1)

        time.sleep(1)  # Pequeno delay para evitar sobrecarga
