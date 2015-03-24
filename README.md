# linsensors: access embedded sensors through linux

**linsensors** is an effort to create a “batteries included” python module for a range of
sensors that can be accessed through standard linux interfaces.

## Installation
linsensors works for both python 2 and 3

```
pip install linsensors
```

Additionally, you may want to install modbus, a library used for several of the sensors
In order to get these, you must install modbus’s dependencies

**On Debian / Ubuntu**
```
sudo apt-get install python-dev  # or python3-dev
sudo apt-get install libffi-dev
pip install modbus
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

