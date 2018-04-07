# -*- coding: utf-8 -*-
"""This module contains "unit" tests for ```spiders.py```."""

import json
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

    def test_load_sample_spiders(self):
        p = subprocess.Popen(
            ['spiders.py', '--samples'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        (stdout_and_stderr, _) = p.communicate()
        self.assertEqual(p.returncode, 0)
        expected_stdout_and_stderr = {
          "cloudfeaster.samples.pypi.PyPISpider": {
            "url": "https://pypi.python.org/pypi",
            "identifying_factors": {
              "username": {
                "pattern": "^.+$",
              },
            },
            "authenticating_factors": {
              "password": {
                "pattern": "^.+$",
              },
            },
            "factor_display_order": [
              "username",
              "password",
            ],
            "factor_display_names": {
              "username": {
                "": "username",
                "fr": "Nom d'utilisateur",
                "en": "username",
                "ja": u"ユーザー名",
              },
              "password": {
                "": "password",
                "fr": "mot de passe",
                "en": "Password",
                "ja": u"パスワード",
              }
            },
            "max_concurrent_crawls": 3,
            "max_crawl_time_in_seconds": 30,
            "paranoia_level": "low",
            "ttl_in_seconds": 60,
          },
          "cloudfeaster.samples.pythonwheels_spider.PythonWheelsSpider": {
            "url": "https://pythonwheels.com/",
            "identifying_factors": {},
            "authenticating_factors": {},
            "factor_display_order": [],
            "factor_display_names": {},
            "ttl_in_seconds": 60,
            "paranoia_level": "low",
            "max_concurrent_crawls": 3,
            "max_crawl_time_in_seconds": 30,
          },
          "cloudfeaster.samples.bank_of_canada_daily_exchange_rates.BankOfCanadaDailyExchangeRatesSpider": {
            "url": "http://www.bankofcanada.ca/rates/exchange/daily-exchange-rates/",
            "identifying_factors": {},
            "authenticating_factors": {},
            "factor_display_order": [],
            "factor_display_names": {},
            "ttl_in_seconds": 60,
            "paranoia_level": "low",
            "max_concurrent_crawls": 3,
            "max_crawl_time_in_seconds": 30,
          }
        }
        self.assertEqual(json.loads(stdout_and_stderr), expected_stdout_and_stderr)
