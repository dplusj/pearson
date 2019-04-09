"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from correlation import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=correlation', '--cov-config=./.coveragerc', '--cov-report=term-missing', '-W ignore'])
        raise SystemExit(errno)


setup(
    name = 'correlation',
    version = __version__,
    description = 'A command line program in Python for computing stock correlation.',
    long_description = long_description,
    author = 'Jian Deng',
    author_email = 'jerrydeng.plus@gmail.com',
    license = 'MIT',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: MIT',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6'
    ],
    keywords = 'correlation',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt==0.6.2', 'pandas==0.24.2', 'alpha_vantage==2.1.0', 'matplotlib==3.0.3', 'tables==3.5.1', 'seaborn==0.9.0'],
    extras_require = {
        'test': ['coverage==4.5.3', 'pytest==4.4.0', 'pytest-cov==2.6.1'],
    },
    entry_points = {
        'console_scripts': [
            'compute-correlation=correlation.cli:main',
        ],
    },
    cmdclass = {'test': RunTests},
)
