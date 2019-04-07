"""Tests for our `compute-correlation hello` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase
from correlation.commands.hello import Hello


class TestHello(TestCase):
    def test_returns_multiple_lines(self):
        output = popen(['compute-correlation', 'hello'], stdout=PIPE).communicate()[0].decode("utf-8") 
        lines = output.split('\n')
        self.assertTrue(len(lines) != 1)

    def test_returns_hello_world(self):
        output = popen(['compute-correlation', 'hello'], stdout=PIPE).communicate()[0].decode("utf-8") 
        self.assertTrue('Hello, world!' in output)