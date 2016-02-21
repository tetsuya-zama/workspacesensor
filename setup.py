from setuptools import setup, find_packages
import sys
sys.path.append('./src')

setup(
    name = "WorkspaceSensor",
    version = "0.1",
    packages = find_packages(),
    install_requires=[
        'pubnub'
        'rpi.gpio',
    ]
)
