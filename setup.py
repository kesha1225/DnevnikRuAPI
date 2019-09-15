from setuptools import setup, find_packages
import pydnevnikruapi

setup(
    name='pydnevnikruapi',
    version=pydnevnikruapi.__version__,
    url='https://github.com/kesha1225/DnevnikRuAPI',
    author='kesha1225',
    packages=find_packages(),
    description='simple wrapper for dnevnik.ru API',
    long_description="Информация - https://github.com/kesha1225/DnevnikRuAPI/blob/master/README.md",
    install_requires=['requests']
)