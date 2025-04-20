from setuptools import find_packages
from setuptools import setup

setup(
    name='rasa_hand_pkg',
    version='0.0.0',
    packages=find_packages(
        include=('rasa_hand_pkg', 'rasa_hand_pkg.*')),
)
