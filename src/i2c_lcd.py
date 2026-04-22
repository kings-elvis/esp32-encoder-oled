from lcd_api import LcdApi
import time

class I2cLcd(LcdApi):
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.backlight = 0x08

        self._write_init(0x03)
        time.sleep_ms(5)
        self._write_init(0x03)
        time.sleep_ms(5)
        self._write_init(0x03)
        time.sleep_ms(1)
        self._write_init(0x02)

        super().__init__(num_lines, num_columns)

        self.hal_write_command(0x28)
        self.hal_write_command(0x0C)
        self.clear()

    def _write_init(self, nibble):
        self.i2c.writeto(self.i2c_addr, bytearray([nibble << 4 | self.backlight]))
        self._pulse_enable(nibble << 4)

    def hal_write_command(self, cmd):
        self._write_byte(cmd, 0)

    def hal_write_data(self, data):
        self._write_byte(data, 1)

    def _write_byte(self, byte, mode):
        high = mode | (byte & 0xF0) | self.backlight
        low = mode | ((byte << 4) & 0xF0) | self.backlight

        self.i2c.writeto(self.i2c_addr, bytearray([high]))
        self._pulse_enable(high)

        self.i2c.writeto(self.i2c_addr, bytearray([low]))
        self._pulse_enable(low)

    def _pulse_enable(self, data):
        self.i2c.writeto(self.i2c_addr, bytearray([data | 0x04]))
        time.sleep_us(1)
        self.i2c.writeto(self.i2c_addr, bytearray([data & ~0x04]))
        time.sleep_us(50)