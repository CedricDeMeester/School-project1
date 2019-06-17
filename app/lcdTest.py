import time
from RPi import GPIO
import socket
import fcntl
import struct
import netifaces
from subprocess import check_output

import RPi.GPIO as GPIO

class LCD:
    def __init__(self, datapins:list, rs=21, e=20, isfourbits=False):
        self._isFourBits = isfourbits
        self._rs = rs
        self._e = e
        self._datapins = datapins
        self.function_set = 0x38
        self.display_on = 0x0C
        self.clear_display = 0x01

        self._cursor = False
        self._blinking = False

        self.init_gpio()

        self.init_lcd()

    def init_gpio(self):
        for pin in self._datapins:
            GPIO.setup(pin, GPIO.OUT)
        GPIO.setup(self._rs, GPIO.OUT)
        GPIO.setup(self._e, GPIO.OUT)

    def send_instruction(self, value):
        GPIO.output(self._rs, 0)
        self.set_data_bits(value)
        GPIO.output(self._rs, 0)

    def send_character(self, value):
        GPIO.output(self._rs, 1)
        self.set_data_bits(value)
        GPIO.output(self._rs, 0)

    def set_data_bits(self, value):
        GPIO.output(self._e, 1)
        for i in range(8):
            GPIO.output(self._datapins[i], value >> i & 1)
        time.sleep(0.01)
        GPIO.output(self._e, 0)

    def init_lcd(self):
        self.send_instruction(self.function_set)
        self.send_instruction(self.display_on)
        self.send_instruction(self.clear_display)

    def write_message(self, string):
        for i in range(len(string)):
            if i == 16:
               self.send_instruction(0x80 | 0x40)
            byte = ord(string[i])
            self.send_character(byte)

    def toggle_cursor(self):
        self._cursor = not self._cursor
        if self._cursor:
            self.display_on |= 0x02
        else:
            self.display_on ^= 0x02
        self.send_instruction(self.display_on)

    def toggle_blinking(self):
        self._blinking = not self._blinking
        if self._blinking:
            self.display_on |= 0x01
        else:
            self.display_on ^= 0x01
        self.send_instruction(self.display_on)


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.IN)
    counter = 0

def main():
    try:
        setup()

        datapins = [16, 12, 25, 24, 23, 26, 19, 13]
        lcd1 = LCD(datapins)
        ip = check_output(['hostname', '--all-ip-addresses']).split()
        ip1 = str(ip[0])[2:-1]
        output = ip1
        lcd1.write_message(output)

        while True:
            if output == "tc":
                lcd1.toggle_cursor()
            elif output == "tb":
                lcd1.toggle_blinking()

    except KeyboardInterrupt:
        print("Ok bye!")
    except Exception as ex:
        print("Error! " + str(ex))
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
