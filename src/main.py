from machine import Pin, I2C
from i2c_lcd import I2cLcd
import time

# ------------------------
# I2C LCD SETUP
i2c = I2C(0, scl=Pin(7), sda=Pin(6), freq=400000)

print("I2C scan:", i2c.scan())

I2C_ADDR = 0x27
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# ------------------------
# ENCODER
clk = Pin(2, Pin.IN, Pin.PULL_UP)
dt  = Pin(3, Pin.IN, Pin.PULL_UP)
sw  = Pin(4, Pin.IN, Pin.PULL_UP)

last_clk = clk.value()

# ------------------------
# STATES
MAIN_MENU = 0
SUB_MENU = 1
EDIT = 2

state = MAIN_MENU

main_index = 0
sub_index = 0

# ------------------------
# DATA
temp = [10, 30]
hum = [40, 80]
volt = [3, 5]

main_menu = ["View", "Temp", "Hum", "Volt"]
sub_menu = ["Low", "High", "Back"]

# ------------------------
def display(line1, line2):
    lcd.move_to(0, 0)
    lcd.putstr(" " * 16)
    lcd.move_to(0, 0)
    lcd.putstr(line1[:16])

    lcd.move_to(0, 1)
    lcd.putstr(" " * 16)
    lcd.move_to(0, 1)
    lcd.putstr(line2[:16])

# ------------------------
def get_value(i):
    if main_index == 1:
        return temp[i]
    elif main_index == 2:
        return hum[i]
    elif main_index == 3:
        return volt[i]
    return 0

# ------------------------
def adjust_value(direction):
    if sub_index == 2:
        return

    if main_index == 1:
        temp[sub_index] += direction
    elif main_index == 2:
        hum[sub_index] += direction
    elif main_index == 3:
        volt[sub_index] += direction

# ------------------------
def draw():
    if state == MAIN_MENU:
        display("MAIN MENU", ">" + main_menu[main_index])

    elif state == SUB_MENU:
        if sub_index < 2:
            val = get_value(sub_index)
            display(main_menu[main_index],
                    ">" + sub_menu[sub_index] + ":" + str(val))
        else:
            display(main_menu[main_index], ">BACK")

    elif state == EDIT:
        val = get_value(sub_index)
        display("EDIT " + sub_menu[sub_index],
                "Val:" + str(val))

# ------------------------
# ✅ FIXED ENCODER (THIS IS THE IMPORTANT PART)
def handle_encoder():
    global last_clk, main_index, sub_index

    current_clk = clk.value()

    # detect change
    if current_clk != last_clk:

        # direction detection (reliable for Wokwi)
        if dt.value() != current_clk:
            direction = 1   # clockwise
        else:
            direction = -1  # anti-clockwise

        if state == MAIN_MENU:
            main_index = (main_index + direction) % 4

        elif state == SUB_MENU:
            sub_index = (sub_index + direction) % 3

        elif state == EDIT:
            adjust_value(direction)

    last_clk = current_clk

# ------------------------
# BUTTON
last_btn_time = 0

def handle_button():
    global state, sub_index, last_btn_time

    if sw.value() == 0:
        now = time.ticks_ms()

        if time.ticks_diff(now, last_btn_time) > 250:

            if state == MAIN_MENU:
                if main_index != 0:
                    state = SUB_MENU
                    sub_index = 0

            elif state == SUB_MENU:
                if sub_index == 2:
                    state = MAIN_MENU
                else:
                    state = EDIT

            elif state == EDIT:
                state = SUB_MENU

            last_btn_time = now

# ------------------------
# MAIN LOOP
while True:
    handle_encoder()
    handle_button()
    draw()
    time.sleep_ms(80)