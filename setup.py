try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from linsensors import __version__

config = {
    'name': 'linsensors',
    'author': 'Garrett Berg',
    'author_email': 'garrett@cloudformdesign.com',
    'version': __version__,
    'packages': ['linsensors'],
    'license': 'MIT',
    'install_requires': [
        'i2cdev',
        'pyserial',
    ],
    'extras_require': {
        'spi': ['smbus', 'spidev'],
    },
    'description': "Interface with embedded sensors in linux through i2c, spi, etc",
    'url': "https://github.com/cloudformdesign/linsensors",
    'classifiers': [
        # 'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
}

setup(**config)
