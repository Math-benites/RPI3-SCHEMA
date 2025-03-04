import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017

# Inicializa o barramento I2C e o MCP23017
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c, address=0x20)  # Endereço padrão 0x20
