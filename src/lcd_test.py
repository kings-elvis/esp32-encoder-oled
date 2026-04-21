from machine import Pin, I2C
import time

# LCD address
ADDR = 0x27

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
time.sleep(1)

def write(cmd):
    i2c.writeto(ADDR, bytearray([cmd]))

# Try simple wake-up pulses
for i in range(3):
    write(0x30)
    time.sleep_ms(5)

write(0x20)  # 4-bit mode

time.sleep(1)

# This WILL NOT fully show text yet,
# but confirms communication stability
print("LCD communication OK")