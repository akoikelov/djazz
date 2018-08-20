from distutils.core import setup
import os


##this code taken from django-extensions project
packages, package_data = [], {}

root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
extensions_dir = 'akoikelov'


def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

for dirpath, dirnames, filenames in os.walk(extensions_dir):
    # Ignore PEP 3147 cache dirs and those whose names start with '.'
    dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '__pycache__']
    parts = fullsplit(dirpath)
    package_name = '.'.join(parts)
    if '__init__.py' in filenames:
        packages.append(package_name)
    elif filenames:
        relative_path = []
        while '.'.join(parts) not in packages:
            relative_path.append(parts.pop())
        relative_path.reverse()
        path = os.path.join(*relative_path)
        package_files = package_data.setdefault('.'.join(parts), [])
        package_files.extend([os.path.join(path, f) for f in filenames])


setup(
    name='akoikelov.djazz',
    version='0.0.6',
    packages=packages,
    package_data=package_data,
    include_package_data=True,
    install_requires=['django', 'setuptools', 'mock', 'dropbox', 'unidecode'],
    url='https://github.com/akoikelov/djazz',
    license='',
    author='akoikelov',
    author_email='kolyakoikelov@gmail.com',
    description='Djazz is helper library for Django framework',
)
