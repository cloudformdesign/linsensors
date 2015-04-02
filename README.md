# linsensors: access embedded sensors through linux

**linsensors** is an effort to create a “batteries included” python module for a range of
sensors that can be accessed through standard linux interfaces.

## Installation
linsensors works for both python 2 and 3

```
pip install linsensors
```

Additionally, you may want to install spi funcctionality, which is required to interface with
several sensors.

In order to get these, you must first install modbus’s dependencies

**On Debian / Ubuntu**
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

