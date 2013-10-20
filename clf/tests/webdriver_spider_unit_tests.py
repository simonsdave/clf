"""This module contains unit tests for the ```webdriver_spider``` module."""

import BaseHTTPServer
import os
import SimpleHTTPServer
import sys
import threading
import time
import unittest
import uuid

import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import spider
import webdriver_spider

class TestSpider(unittest.TestCase):
    """A series of unit tests that validate ```webdriver_spider.Spider```."""

    def test_crawl_args_and_return_value_passed_correctly(self):

        self.my_url = "http://www.example.com"
        self.my_arg1 = str(uuid.uuid4())
        self.my_arg2 = str(uuid.uuid4())
        self.mock_browser = None

        def browser_class_patch(url):
            self.assertEqual(url, self.my_url)
            self.assertIsNone(self.mock_browser)
            self.mock_browser = mock.Mock()
            self.mock_browser.__enter__ = mock.Mock(return_value=self.mock_browser)
            self.mock_browser.__exit__ = mock.Mock(return_value=True)
            return self.mock_browser

        with mock.patch("webdriver_spider.Browser", browser_class_patch):

            self.crawl_rv = spider.CrawlResponse(spider.SC_OK)

            class MySpider(webdriver_spider.Spider):
                def crawl(my_spider_self, browser, arg1, arg2):
                    return self.crawl_rv

            my_spider = MySpider(self.my_url)
            walk_rv = my_spider.walk(self.my_arg1, self.my_arg2)
            self.assertIsNotNone(walk_rv)
            self.assertEqual(walk_rv, self.crawl_rv)

            self.assertIsNotNone(self.mock_browser)
            self.assertEqual(self.mock_browser.__enter__.call_count, 1)
            self.assertEqual(self.mock_browser.__exit__.call_count, 1)




class HTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """Only reason this class exists is to stop writing of log messages
    to stdout as part of serving up documents."""

    def log_message(format, *arg):
        """yes this really is meant to be a no-op"""
        pass

    def do_GET(self):
        key = self.path[1:]
        html = HTTPServer.html_pages.get(key, None)
        if html:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(html))
            self.end_headers()
            self.wfile.write(html)
        else:
            self.send_response(404)


class HTTPServer(threading.Thread):

    html_pages = {}

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        httpdAddress = ('', 0)
        httpd = BaseHTTPServer.HTTPServer(
            httpdAddress,
            HTTPRequestHandler )
        self.portNumber = httpd.server_port
        httpd.serve_forever()
        "never returns"

    def start(self):
        threading.Thread.start(self)
        "give the HTTP server time to start & initialize itself"
        while 'portNumber' not in self.__dict__:
            time.sleep(1)

class TestBrowser(unittest.TestCase):
    """A series of unit tests that validate ```webdriver_spider.Browser```."""

    @classmethod
    def setUpClass(cls):
        cls._httpServer = HTTPServer()
        cls._httpServer.start()

    @classmethod
    def tearDownClass( cls ):
        cls._httpServer = None

    def test_is_element_present(self):
        """Validate ```webdriver_spider.Browser.is_element_present```."""
        html = (
            '<html>'
            '<title>Dave Was Here!!!</title>'
            '<body>'
            '<h1 id=42>Dave Was Here!!!</h1>'
            '</body>'
            '</html>'
        )
        page = "testIsElementPresent.html"
        HTTPServer.html_pages[page] = html
        url = "http://127.0.0.1:%d/%s" % (
            type(self)._httpServer.portNumber,
            page
        )
        with webdriver_spider.Browser(url) as browser:
            enoughTimeForPageToLoad = 5
            time.sleep(enoughTimeForPageToLoad)
            self.assertTrue(browser.is_element_present("//h1[@id='42']"))
            self.assertFalse(browser.is_element_present("//h1[@id='43']"))
