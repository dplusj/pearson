"""Tests for the main CLI module."""

from subprocess import PIPE, Popen as popen
from unittest import TestCase, mock

from correlation import __version__ as VERSION
from correlation.cli import main


class TestHelp(TestCase):
    @mock.patch('configparser.ConfigParser')
    def test_call_compute_run(self, mock_configparser):
        options = {
            '--start-date' : '2018-08-08',
            '--last-date' : '2018-08-10',
            '--stocks' : 'UNIVERSE.ABC'
        }
        with mock.patch('docopt.docopt') as mocked_docopt:
            mocked_docopt.return_value = options
            cp = mock_configparser()
            cp.read.return_value = None
            with mock.patch('correlation.commands.compute.Compute') as mock_compute:
                with mock.patch('correlation.datafusion.DataFusion') as mock_datafusion:
                    mc = mock_compute()
                    mc.run.return_value = None
                    main()
                    mc.run.assert_called_once()
