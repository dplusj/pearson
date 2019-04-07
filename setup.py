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
        errno = call(['py.test', '--cov=correlation', '--cov-report=term-missing', '-W ignore'])
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
    install_requires = ['docopt', 'pandas', 'alpha_vantage', 'matplotlib', 'tables'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'compute-correlation=correlation.cli:main',
        ],
    },
    cmdclass = {'test': RunTests},
)
