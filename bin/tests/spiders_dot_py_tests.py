"""This module contains "unit" tests for ```spiders.py```."""

import subprocess
import unittest

from nose.plugins.attrib import attr


@attr('integration')
class TestSpidersDotPy(unittest.TestCase):

    def test_all_good(self):
        p = subprocess.Popen(
            ['spiders.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        (stdout_and_stderr, _) = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertEqual(stdout_and_stderr, '{}\n')

    def test_invalid_command_line_args(self):
        p = subprocess.Popen(
            ['spiders.py', 'dave-creates-an-error'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        (stdout_and_stderr, _) = p.communicate()
        self.assertEqual(p.returncode, 2)
        self.assertEqual(
            stdout_and_stderr,
            'Usage: spiders.py [options] <package>\n\nspiders.py: error: try again ...\n')
