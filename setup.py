# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='TumbleTrack',
      version='1.0',
      description='Tumbleweed Main Software',
      url='https://github.com/austrian-code-wizard/TumbleTrack',
      author='Moritz Stephan',
      author_email='moritz@teamtumbleweed.eu',
      license='MIT',
      packages=['twABCs', 'twDevices', 'twParser', 'twModules', 'twHandler', 'twExceptions'],
      install_requires=['Adafruit-GPIO', 'Adafruit-PureIO', 'gps', 'numpy', 'pyserial', 'Cython'],
      zip_safe=False)

