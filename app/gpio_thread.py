import time
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017
import threading

def gpio_task():
    # Inicializa o barramento I2C:
    i2c = busio.I2C(board.SCL, board.SDA)

    # Cria uma instância do MCP23017 (endereço 0x20):
    mcp = MCP23017(i2c, address=0x20)

    # Obtém as instâncias dos pinos GPIO
    pin0 = mcp.get_pin(0)
    pin1 = mcp.get_pin(1)

    # Configura o pin0 como saída com valor alto (ligado)
    pin0.switch_to_output(value=True)

    # Configura o pin1 como entrada com resistor pull-up ativado
    pin1.direction = digitalio.Direction.INPUT
    pin1.pull = digitalio.Pull.UP

    # Loop que pisca o pino 0 e lê o valor do pino 1
    while True:
        # Pisca o pino 0
        pin0.value = True
        print("Pin 1 is at a HIGH level: {0}".format(pin1.value))
        time.sleep(1.5)
        pin0.value = False
        print("Pin 1 is at a low level: {0}".format(pin1.value))
        time.sleep(1.5)
