from machine import Pin, I2C
import time

# OLED init (safe)
oled = None

try:
    import ssd1306
    i2c = I2C(0, scl=Pin(9), sda=Pin(8))

    if 60 in i2c.scan():
        oled = ssd1306.SSD1306_I2C(128, 64, i2c)
        print("OLED detected")
    else:
        print("OLED not found")

except:
    print("OLED init failed")

# Encoder
clk = Pin(2, Pin.IN, Pin.PULL_UP)
dt = Pin(3, Pin.IN, Pin.PULL_UP)
sw = Pin(4, Pin.IN, Pin.PULL_UP)

last_clk = clk.value()

# Menu
main_index = 0
menu = ["View", "Temp", "Humidity", "Voltage"]

def draw():
    if not oled:
        return

    oled.fill(0)
    oled.text("MAIN MENU", 0, 0)

    for i in range(len(menu)):
        prefix = ">" if i == main_index else " "
        oled.text(prefix + menu[i], 0, 10 + i * 10)

    oled.show()

def encoder():
    global last_clk, main_index

    current = clk.value()

    if last_clk == 1 and current == 0:
        direction = 1 if dt.value() else -1
        main_index = (main_index + direction) % len(menu)

    last_clk = current

while True:
    encoder()
    draw()
    time.sleep(0.05)