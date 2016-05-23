from distutils.core import setup
from setuptools import find_packages

setup(
    name='akoikelov.djazz',
    version='1.0',
    packages=find_packages(),
    package_data={'akoikelov.djazz.management.commands.skeleton': ['*.skeleton']},
    include_package_data=True,
    url='https://github.com/akoikelov/djazz',
    license='',
    author='akoikelov',
    author_email='kolyakoikelov@gmail.com',
    description='Djazz is helper library for Django framework'
)
