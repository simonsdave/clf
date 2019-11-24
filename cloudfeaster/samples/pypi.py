#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This spider attempts to login to pypi with a username and password
supplied at runtime. This sample is intended to illustrate how to
work with identifying and authenticating factors. The key thing to
focus on with this spider is get_metadata().
"""

import json
import sys

from selenium.webdriver.support.ui import WebDriverWait

from cloudfeaster import spider


class PyPISpider(spider.Spider):

    @classmethod
    def get_metadata(cls):
        return {
            'url': 'https://pypi.python.org/pypi',
            'identifyingFactors': {
                'username': {
                    'pattern': '^.+$',
                },
            },
            'authenticatingFactors': {
                'password': {
                    'pattern': '^.+$',
                },
            },
            'factorDisplayOrder': [
                'username',
                'password'
            ],
            'factorDisplayNames': {
                'username': {
                    'en': 'username',
                    'fr': "nom d'utilisateur",
                    'ja': 'ユーザー名',
                },
                'password': {
                    'en': 'password',
                    'fr': 'mot de passe',
                    'ja': 'パスワード',
                },
            },
        }

    def crawl(self, browser, username, password):
        ten_seconds = 10
        web_driver_wait = WebDriverWait(browser, ten_seconds)

        xpath = '//a[text()="Log in"]'
        login_link_element = web_driver_wait.until(lambda browser: browser.find_element_by_xpath(xpath))
        login_link_element.click()

        xpath = '//input[@name="username"]'
        username_input_element = web_driver_wait.until(lambda browser: browser.find_element_by_xpath(xpath))
        username_input_element.send_keys(username)

        xpath = '//input[@name="password"]'
        password_input_element = web_driver_wait.until(lambda browser: browser.find_element_by_xpath(xpath))
        password_input_element.send_keys(password)

        xpath = '//input[@value="Log in"]'
        login_input_element = web_driver_wait.until(lambda browser: browser.find_element_by_xpath(xpath))
        login_input_element.click()

        login_successful_xpath = '//h3[text()="Your account"]'
        bad_credentials_xpath = '//li[contains(text(),"The password is invalid. Try again.")]'
        bad_login_crawl_response = browser.wait_for_login_to_complete(
            login_successful_xpath,
            bad_credentials_xpath)
        if bad_login_crawl_response:
            return bad_login_crawl_response

        xpath = '//button[contains(text(),{username})]/..'.format(username=username)
        menu_button_element = web_driver_wait.until(lambda browser: browser.find_element_by_xpath(xpath))
        menu_button_element.click()

        xpath = '//button[contains(text(),"Log out")]'
        logout_link_element = web_driver_wait.until(lambda browser: browser.find_element_by_xpath(xpath))
        logout_link_element.click()

        xpath = '//a[text()="Log in"]'
        login_link_element = web_driver_wait.until(lambda browser: browser.find_element_by_xpath(xpath))

        return spider.CrawlResponseOk({})


if __name__ == '__main__':
    crawl_debugger = spider.CrawlDebugger()
    crawl_args = spider.CLICrawlArgs(PyPISpider)
    crawler = spider.SpiderCrawler(PyPISpider, crawl_debugger.debug)
    crawl_result = crawler.crawl(*crawl_args)
    print json.dumps(crawl_result)
    sys.exit(1 if crawl_result.status_code else 0)
