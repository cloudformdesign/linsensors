#!/usr/bin/env python

# Copyright 2015 Garrett Berg, n.io. All rights reserved.
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

import time
from i2cdev import I2C
import struct

DATA_FORMAT = '!BHB'

I2C_SLAVE = 0x0703
AI418S_ADDR = 0x68
STD_CONFIG = '1{}011{}'.format  # std config, call it with the channel (00, 01, etc)
tobin = '{:02b}'.format

PGA = {
    1: '00',
    2: '01',
    4: '10',
    8: '11'
}


class AI418S(object):
    def __init__(self, channel, pga=None, current=None):
        self.channel = channel
        self.dev = I2C(AI418S_ADDR, 1, I2C_SLAVE)
        self._pga = pga
        self._current = current

    def read(self, pga=None, current=None):
        if pga is None:
            pga = 1 if self._pga is None else self._pga
        if current is None:
            current = True if self._current is None else self._current
        if pga not in PGA: raise ValueError(pga)
        config_str = STD_CONFIG(tobin(self.channel), PGA[pga])
        config_int = int(config_str, 2)
        config = bytes([config_int])
        self.dev.write(config)
        time.sleep(1)
        data = self.dev.read(4)
        data = struct.unpack(DATA_FORMAT, data)
        value = data[1] + ((data[0] & 0x03) << 16)
        config = data[2]
        value = (value / 131071) * (2.048 / pga) * (180 / 33)
        if current:
            value = value / 249
        return value


if __name__ == '__main__':
    print("running")
    dev = AI418S(0)
    while True:
        print("Value: ", dev.read(2))

