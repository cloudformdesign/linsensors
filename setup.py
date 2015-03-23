try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from cloudtb import __version__

config = {
    'name': 'embedded_sensors',
    'author': 'Garrett Berg',
    'author_email': 'garrett@cloudformdesign.com',
    'version': __version__,
    'packages': ['embedded_sensors'],
    'license': 'MIT',
    'install_requires': [
        'spidev',
        'i2cdev',
    ],
    'extras_require': {
        'smbus': ['smbus'],
    },
    'description': "Interface with embedded sensors through i2c, spi, etc",
    'url': "https://github.com/cloudformdesign/embedded_sensors",
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
