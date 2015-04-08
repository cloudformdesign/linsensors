# linsensors: access embedded sensors through linux

**linsensors** is an effort to create a “batteries included” python module for a range of
sensors that can be accessed through standard linux interfaces.

## Installation
linsensors works for both python 2 and 3

```
pip install linsensors
```

#### Raspberry Pi

- Follow [these directions] to enable I2C

Make the following files look like: (from [here](http://www.modmypi.com/blog/loading-i2c-spi-and-1-wire-drivers-on-the-raspberry-pi-under-raspbian-wheezy))

This also enables i2c, 1-wire and 1-wire-thermometers

- `nano /etc/modprobe.d/raspi-blacklist.conf`:
```
# blacklist spi and i2c by default (many users don’t need them)
blacklist spi-bcm2708
blacklist i2c-bcm2708
```
- `nano /etc/modules` :
```
# /etc/modules: kernel modules to load at boot time.
#
# This file contains the names of kernel modules that should be loaded
# at boot time, one per line. Lines beginning with “#” are ignored.
# Parameters can be specified after the module name.
#
# sound devices
snd-bcm2835
# SPI devices
spi-dev
# I2C devices
i2c-dev
# 1-Wire devices
w1-gpio
# 1-Wire thermometer devices
w1-therm
```

#### Installing required libraries for python modules
**On Debian/Ubuntu**
```
sudo apt-get install python-dev  # or python3-dev
sudo apt-get install libffi-dev
```
Then install linsensors with spi
```
pip install linsensors[spi]
```

## Use
check out each file for details on how to use. Most sensors are used something like:

```
from linsensors.htu21d import Htu21d
htu = Htu21d(0)
temperature = htu.temperature
humidity = htu.humidity

# do something with temp/humidity
```

