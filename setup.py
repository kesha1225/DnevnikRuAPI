from setuptools import setup, find_packages
import pydnevnikruapi

setup(
    name='pydnevnikruapi',
    version=pydnevnikruapi.__version__,
    url='https://github.com/kesha1225/DnevnikRuAPI',
    author='kesha1225',
    packages=find_packages(),
    description='simple wrapper for dnevnik.ru API',
    python_requires='>=3.7.0',
    install_requires=['requests'],
    include_package_data=True
)