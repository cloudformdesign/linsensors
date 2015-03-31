#!/usr/bin/env python

# Copyright 2014 IIJ Innovation Institute Inc. All rights reserved.
# Copyright 2014 Keiichi Shima. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''A Python class to access HTU21D based relative humidity sensor
provided by SWITCHSCIENCE as a part no. SFE-SEN-12064.

Example:

bus = 1
sensor = htu21d.Htu21d(bus)
print(sensor.humidity)

'''

import time
import array

from i2cdev import I2C

I2C_SLAVE = 0x0703
HTU21D_ADDR = 0x40
CMD_READ_TEMP_HOLD = b"\xE3"
CMD_READ_HUM_HOLD = b"\xE5"
CMD_READ_TEMP_NOHOLD = b"\xF3"
CMD_READ_HUM_NOHOLD = b"\xF5"
CMD_WRITE_USER_REG = b"\xE6"
CMD_READ_USER_REG = b"\xE7"
CMD_SOFT_RESET = b"\xFE"


class Htu21d(object):
    def __init__(self, address):
        self.dev = I2C(HTU21D_ADDR, 1, address)  # HTU21D 0x40, bus 1
        with self.dev.lock:
            self.dev.write(CMD_SOFT_RESET)  # soft reset
        time.sleep(.1)

    def ctemp(self, sensorTemp):
        tSensorTemp = sensorTemp / 65536.0
        return -46.85 + (175.72 * tSensorTemp)

    def chumid(self, sensorHumid):
        tSensorHumid = sensorHumid / 65536.0
        return -6.0 + (125.0 * tSensorHumid)

    def crc8check(self, value):
        # Ported from Sparkfun Arduino HTU21D Library: https://github.com/sparkfun/HTU21D_Breakout
        remainder = ((value[0] << 8) + value[1]) << 8
        remainder |= value[2]

        # POLYNOMIAL = 0x0131 = x^8 + x^5 + x^4 + 1
        # divsor = 0x988000 is the 0x0131 polynomial shifted to farthest left of three bytes
        divsor = 0x988000

        for i in range(0, 16):
            if(remainder & 1 << (23 - i)):
                remainder ^= divsor
            divsor = divsor >> 1

        if remainder == 0:
            return True
        else:
            return False

    def read_temperature(self):
        with self.dev.lock:
            self.dev.write(CMD_READ_TEMP_NOHOLD)  # measure temp
            time.sleep(.1)

            data = self.dev.read(3)
        buf = array.array('B', data)

        if self.crc8check(buf):
            temp = (buf[0] << 8 | buf[1]) & 0xFFFC
            return self.ctemp(temp)
        else:
            return -255

    def read_humidity(self):
        with self.dev.lock:
            self.dev.write(CMD_READ_HUM_NOHOLD)  # measure humidity
            time.sleep(.1)

            data = self.dev.read(3)
        buf = array.array('B', data)

        if self.crc8check(buf):
            humid = (buf[0] << 8 | buf[1]) & 0xFFFC
            return self.chumid(humid)
        else:
            return -255

if __name__ == "__main__":
    obj = HTU21D(I2C_SLAVE)
    print("Temp:", obj.read_temperature(), "C")
    print("Humid:", obj.read_humidity(), "% rH")
