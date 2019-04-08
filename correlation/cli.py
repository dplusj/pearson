"""
compute-correlation
Usage:
  compute-correlation --start-date=<sd> --last-date=<ld> --stocks=<ss> [--plot]
  compute-correlation -h | --help
  compute-correlation --version
Options:
  -h --help                         Show this screen.
  --version                         Show version.
Examples:
  compute-correlation --start-date=2015-01-01 --last-date=2019-01-11 --stocks=AAPL,MSFT,GOOG --plot
"""

import os
import configparser
from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION
from . import datafusion as engine


def main():
    """Main CLI entrypoint."""
    options = docopt(__doc__, version=VERSION)
    configPath = os.path.expanduser('~/.correlationrc')
    if not os.path.exists(configPath):
        raise ValueError('Missing default configuration file ~/.correlationrc')

    config = configparser.ConfigParser()
    config.read(configPath, encoding="utf-8")
    apiKey = config['DEFAULT']['APIKEY']
    storePath = config['DEFAULT']['STOREPATH']
    dataFusion = engine.DataFusion(storePath, apiKey)

    try:
        from correlation.commands.compute import Compute 
        calculator = Compute(dataFusion, options)
        calculator.run()
    except ValueError as error:
        print(error)
    except Exception as e:
        print(e)
    except:
        print('Compute correlation failed due to unknown reason')
    finally:
        dataFusion.exit()