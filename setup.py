from distutils.core import setup

setup(
    name='djazz',
    version='1.0',
    packages=['akoikelov', 'akoikelov.djazz',
              'akoikelov.djazz.management', 'akoikelov.djazz.management.commands',
              'akoikelov.djazz.management.commands.generators'],
    url='https://github.com/akoikelov/djazz',
    license='',
    author='akoikelov',
    author_email='kolyakoikelov@gmail.com',
    description='Djazz is helper library for Django framework'
)
