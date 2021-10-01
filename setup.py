import sys
from setuptools import setup
import src as kt

sys.path.append('./src')
sys.path.append('./tests')

setup(
    version = kt.__version__,
    license = kt.__license__,
    author = kt.__author__,
    url = kt.__url__,
)
