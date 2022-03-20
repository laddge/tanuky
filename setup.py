from setuptools import setup
from tanuky import __version__

try:
    with open('README.md') as f:
        readme = f.read()
except IOError:
    readme = ''

setup(
    name='tanuky',
    version=__version__,
    description='simple & flexible SSG',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/laddge/tanuky',
    author='Laddge',
    author_email='dev.laddge@gmail.com',
    licence='MIT',
    packages=['tanuky']
)
