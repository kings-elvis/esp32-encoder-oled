from machine import Pin, I2C
from i2c_lcd import I2cLcd
import time

i2c = I2C(0, scl=Pin(8), sda=Pin(9), freq=100000)

time.sleep(1)  # <<< IMPORTANT

lcd = I2cLcd(i2c, 39, 2, 16)

lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("LCD WORKING")

lcd.move_to(0, 1)
lcd.putstr("ESP32-C3")

while True:
    pass