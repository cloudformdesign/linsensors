#!/usr/bin/env python

# Copyright 2015      Garrett Berg, n.io. All rights reserved.
# Copyright 2012-2013 Limor Fried, Kevin Townsend and Mikey Sklar
#   for Adafruit Industries. All rights reserved.
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

from __future__ import division, print_function
import i2cdev


# get the datasheet for this sensor here:
#   https://cdn.sparkfun.com/datasheets/BreakoutBoards/MCP4725_2009.pdf
# Table 5-2
PD = {
    0: 'normal',
    1: '1k',
    2: '100k',
    3: '500k'
}


class MCP4725 :
    # Registers
    __REG_WRITEDAC         = 0x40
    __REG_WRITEDACEEPROM   = 0x60

    # Constructor
    def __init__(self, bus, address, vcc=3.3):
        self.vcc = vcc
        self._i2c = i2cdev.I2C(address, bus)

    def setVoltage(self, voltage, persist=False):
        "Sets the output voltage to the specified value"
        if voltage > self.vcc:
            voltage = self.vcc
        if voltage < 0:
            voltage = 0

        voltage = int(round(4095 * voltage / self.vcc, 0))
        # Value needs to be left-shifted four bytes for the MCP4725
        if (persist):
            data = [self.__REG_WRITEDACEEPROM]
        else:
            data = [self.__REG_WRITEDAC]
        data.extend([(voltage >> 4) & 0xFF, (voltage << 4) & 0xFF])
        self._i2c.write(bytes(data))

    def readStatus(self):
        data = self._i2c.read(5)
        status = data[0]
        status = {
            'bsy': bool(0x80 & status),
            'por': bool(0x40 & status),
            'pd': PD[0b110 & status >> 1],
        }
        dac = ((data[1] & 0xFF) << 4) + ((data[2] & 0xFF) >> 4)
        eeprom = ((data[3] & 0x0F) << 4) + (data[4] & 0xFF)

        return status, dac, eeprom


if __name__ == '__main__':
    # for many versions of the raspi, use bus=0
    # addr=0x60 is the default
    sensor = MCP4725(1, 0x60, vcc=3.402)
    sensor.setVoltage(0.42)
    print(sensor.readStatus())
