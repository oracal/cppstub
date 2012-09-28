try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='cppstub',
    version='0.0.1',
    author='Thomas Whitton',
    author_email='mail@thomaswhitton.com',
    packages=['cppstub'],
    url='https://github.com/oracal/cppstub',
    license='LICENSE.txt',
    description='C++ file stub generator',
    long_description=open('README.md').read(),
)
