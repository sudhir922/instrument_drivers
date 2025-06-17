try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'instrumnet_drivers',
    'author': 'Sudhir Sahu',
    'url': 'https://github.com/sudhir922/instrument_drivers',
    'download_url': 'https://github.com/sudhir922/instrument_drivers.git',
    'author_email': 'sudhir922@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['instrument_drivers'],
    'scripts': [],
    'name': 'instrument_drivers'
}

setup(**config)