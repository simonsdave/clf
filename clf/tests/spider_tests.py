"""This module contains unit tests for the ```spider``` module."""

import hashlib
import inspect
import sys
import unittest
import uuid

from clf import spider


class TestCrawlResponse(unittest.TestCase):

    def test_ctr_with_just_status_code_ok(self):
        status_code = 42
        cr = spider.CrawlResponse(status_code)
        self.assertEqual(cr.status_code, status_code)
        self.assertIsNone(cr.data)
        self.assertIsNone(cr.status)

    def test_ctr_with_status_code_and_status_ok(self):
        status_code = 42
        status = str(uuid.uuid4())
        cr = spider.CrawlResponse(status_code, status=status)
        self.assertEqual(cr.status_code, status_code)
        self.assertIsNone(cr.data)
        self.assertEqual(cr.status, status)

    def test_ctr_with_status_code_status_and_data_ok(self):
        status_code = 42
        status = str(uuid.uuid4())
        data = {
            'data1': str(uuid.uuid4()),
            'data2': str(uuid.uuid4()),
        }
        cr = spider.CrawlResponse(status_code, data, status)
        self.assertEqual(cr.status_code, status_code)
        self.assertEqual(cr.data, data)
        self.assertEqual(cr.status, status)


class TestSpider(unittest.TestCase):

    def test_spider_with_no_crawl_method(self):
        class MySpider(spider.Spider):
            @classmethod
            def metadata(cls):
                return {"url": "http://www.example.com"}
        my_spider = MySpider()
        with self.assertRaises(NotImplementedError):
            my_spider.crawl()

    def test_spider_with_crawl_method_that_raises_exception(self):
        class MySpider(spider.Spider):
            @classmethod
            def metadata(cls):
                return {"url": "http://www.example.com"}
            def crawl(self):
                raise Exception()
        my_spider = MySpider()
        rv = my_spider.walk()
        self.assertIsNotNone(rv)
        self.assertEqual(type(rv), spider.CrawlResponse)
        self.assertEqual(rv.status_code, spider.CrawlResponse.SC_CRAWL_THREW_EXCEPTION)

    def test_spider_with_crawl_method_with_invalid_return_type(self):
        class MySpider(spider.Spider):
            @classmethod
            def metadata(cls):
                return {"url": "http://www.example.com"}
            def crawl(self):
                return None
        my_spider = MySpider()
        rv = my_spider.walk()
        self.assertIsNotNone(rv)
        self.assertEqual(type(rv), spider.CrawlResponse)
        self.assertEqual(rv.status_code, spider.CrawlResponse.SC_INVALID_CRAWL_RETURN_TYPE)

    def test_spider_correctly_passes_crawl_args_and_returns(self):
        my_arg1 = str(uuid.uuid4())
        my_arg2 = str(uuid.uuid4())
        my_crawl_response = spider.CrawlResponse(
            spider.CrawlResponse.SC_OK,
            {
                'data1': str(uuid.uuid4()),
                'data2': str(uuid.uuid4()),
            },
            "all ok!!!"
        )

        class MySpider(spider.Spider):
            @classmethod
            def metadata(cls):
                return {"url": "http://www.example.com"}
            def crawl(the_spider_self, arg1, arg2):
                self.assertEqual(arg1, my_arg1)
                self.assertEqual(arg2, my_arg2)
                return my_crawl_response

        my_spider = MySpider()
        rv = my_spider.walk(my_arg1, my_arg2)
        self.assertIsNotNone(rv)
        self.assertEqual(type(rv), spider.CrawlResponse)
        self.assertEqual(rv, my_crawl_response)

    def test_spider_version(self):
        """Verify clf.Spider.version()."""

        class MySpider(spider.Spider):
            pass

        module = sys.modules[self.__module__]
        source = inspect.getsource(module)
        expected_version = hashlib.sha1(source)
        expected_version = expected_version.hexdigest()
        self.assertEqual(expected_version, MySpider.version())


class TestSpiderMetadata(unittest.TestCase):

    def test_spider_not_implementing_metadata_class_method(self):
        class MySpider(spider.Spider):
            pass
        with self.assertRaises(NotImplementedError):
            MySpider.metadata()

    def test_is_metadata_when_metadata_class_method_not_implemented(self):
        class MySpider(spider.Spider):
            pass
        self.assertFalse(MySpider.is_metadata_ok())

    def test_metadata_all_good(self):
        class MySpider(spider.Spider):
            @classmethod
            def metadata(cls):
                rv = {
                    "url": "http://www.google.com",
                }
                return rv
        MySpider.metadata()
        self.assertTrue(MySpider.is_metadata_ok())
