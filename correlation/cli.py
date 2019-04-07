"""
compute-correlation
Usage:
  compute-correlation hello
  compute-correlation --start-date=<sd> --last-date=<ld> --stocks=<ss> [--plot]
  compute-correlation -h | --help
  compute-correlation --version
Options:
  -h --help                         Show this screen.
  --version                         Show version.
Examples:
  compute-correlation --start-date=2015-01-01 --last-date=2019-01-11 --stocks=AAPL,MSFT,GOOG
  compute-correlation hello
"""

import os, configparser
from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION
from . import datafusion as engine


def main():
    """Main CLI entrypoint."""
    configPath = os.path.expanduser('~/.correlationrc')
    if not os.path.exists(configPath):
        raise ValueError('Missing default configuration file ~/.correlationrc')

    config = configparser.ConfigParser()   # 创建对象
    config.read(configPath, encoding="utf-8") 
    apiKey = config['DEFAULT']['APIKEY']
    storePath = config['DEFAULT']['STOREPATH']
    dataFusion = engine.DataFusion(storePath, apiKey)

    import correlation.commands
    options = docopt(__doc__, version=VERSION)
    extensionMatched = False

    try:
        for (k, v) in options.items(): 
            if hasattr(correlation.commands, k) and v:
                extensionMatched = True
                module = getattr(correlation.commands, k)
                correlation.commands = getmembers(module, isclass)
                command = [command[1] for command in correlation.commands if command[0] != 'Base'][0]
                command = command(options)
                command.run()
    
        if not extensionMatched:
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