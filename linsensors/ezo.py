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
import itertools
from threading import Thread
from collections import deque

import serial
from .tools import decode, encode

class Ezo(object):
    '''Continuously reads the ph meter. Stores available data in
        `self.data` deque, and responses in `self.repsonse` deque

    data should be read with ph.data.pop() or ph.read()

    ph.read() will block until a value is available. It will return the most recent value and clear the data buffer
    '''
    def __init__(self, port='/dev/ttyAMA0', baud=38400, timeout = 0.05):
        self._kill = False
        self._com = serial.Serial(port, baud)
        self._unparsed = b''
        self.data = deque()
        self._response = deque()
        self.timeout = timeout

        self.command('Response', '0')  # disable responses
        self.command('C', '1')  # enable continuous polling
        self.command('L', '1')  # enable leds
        self._com.timeout = 0.15
        self._com.readall()  # flush buffer
        self._com.timeout = timeout

        self._thread = Thread(target = self._read_thread)
        self._thread.daemon = True
        self._thread.start()

    def read(self, timeout=2.1):
        '''Use this to read values from the ph sensor'''
        start = time.time()
        while not self.data:
            time.sleep(0.1)
            if time.time() - start > timeout:
                raise TimeoutError()
        out = self.data.popleft()
        self.data.clear()
        return out

    def set_temperature(self, temperature):
        '''Set Temperature for more accurate ph readings'''
        self.command('T', str(temperature))

    def calibrate(self):
        user = input('This will re-calibrate the device -- are you sure you want to proceed? (y/n): ')
        if user != 'y':
            return

        def get_float(name):
            user = 'n'
            while user != 'y':
                value = 0
                user = 'n'
                try:
                    value = float(input('Submerge in solution and enter the pH {}:'.format(name)))
                    user = input('Is {} correct? (y/n):')
                except ValueError:
                    print("Incorrect Value, try again")
                if not 0 <= value <= 14:
                    print('value must be between 0 and 14')
            return value

        cal = 'Cal'
        mid = get_float('Midpoint')
        if mid is None:
            print("Canceling calibration")
            return
        self.command(cal, 'clear')
        self.command(cal, 'mid', mid)
        low = get_float('Low point')
        if low is not None:
            self.command(cal, 'low', low)
        high = get_float('High Point')
        if high is not None:
            self.command(cal, 'high', high)
        return self.response(cal, '?')

    def _write(self, command):
        command = encode(command)
        self._com.write(command + b'\r')

    def command(self, command, *args):
        command = encode(command)
        args = map(encode, args)
        command = b','.join(itertools.chain((command,), args))
        print("Sending command:", decode(command))
        self._write(command)

    def response(self, *args):
        '''Perform a command and return the response'''
        self._response.clear()
        self.command(self, *args)
        while not self._response:
            time.sleep(0.01)
        out = self._response.popleft()
        self._response.clear()
        return out

    def _read(self):
        return self._com.readall()

    def _parse(self, data):
        data = data.split(b'\r')
        if len(data) == 1:
            self._unparsed = data[0]
            return
        data[0] = b''.join((self._unparsed, data[0]))
        self._unparsed = data.pop()
        for d in data:
            if b'.' in d:
                try:
                    d = float(d)
                    self.data.appendleft(d)
                    continue
                except (TypeError, ValueError):
                    pass
            self._response.appendleft(encode(d))
        self._cleanup()

    def _cleanup(self):
        while len(self.data) > 20:
            self.data.pop()
        while len(self._response) > 20:
            self._response.pop()

    def _read_thread(self):
        sleep_time = 0.2
        time.sleep(sleep_time)
        while not self._kill:
            start = time.time()
            self._parse(self._read())
            try:
                time.sleep(sleep_time - (time.time() - start))
            except ValueError:
                pass

    def __del__(self):
        self._kill = True
