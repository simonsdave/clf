"""This module contains all queues and messages used by a spider host."""

import datetime
import logging

from clf.util.queues import Queue
from clf.util.queues import Message
import clf.spider

_logger = logging.getLogger("CLF_%s" % __name__)


class CrawlRequestQueue(Queue):

    @classmethod
    def get_message_class(cls):
        return CrawlRequest

    @classmethod
    def get_queue_name_prefix(cls):
        return "clf_creq_"


class CrawlRequest(Message):
    """An instance of :py:class:`clf.spider_host.CrawlRequest` represents a request
    for a spider to crawl a web site. After the request has been created
    it is added to a ```CrawlRequestQueue```. A spider host will read
    the request from the ```CrawlRequestQueue``` and write the response
    to a :py:class:`clf.spider_host.CrawlResponseQueue`."""

    @classmethod
    def get_schema(cls):
        additional_properties = {
            "spider_name": {
                "type": "string",
                "minLength": 1,
            },
            "spider_args": {
                "type": "array",
                "items": {
                    "type": "string",
                    "minLength": 1,
                },
            },
        }
        required_properties = [
            "spider_name",
            "spider_args",
        ]
        return Message.get_schema(additional_properties, required_properties)

    # :TODO: might be interesting to not have to pass local_spider_repo
    # but rather construct the local spider repo on the fly by reading
    # the remote spider repo's name from a configuration file.

    def process(self, local_spider_repo):
        metrics = {}

        download_spider_start_time = datetime.datetime.utcnow()
        spider_class = local_spider_repo.get_spider_class(self.spider_name)
        download_spider_end_time = datetime.datetime.utcnow()

        self._add_timing_entry_to_metrics_dict(
            metrics,
            download_spider_start_time,
            download_spider_end_time,
            "download_spider")

        if not spider_class:
            status = "Unknown spider '%s'" % self.spider_name
            crawl_response = clf.spider.CrawlResponse(
                clf.spider.SC_SPIDER_NOT_FOUND,
                status=status
            )
            rv = CrawlResponse(
                uuid=self.uuid,
                spider_name=self.spider_name,
                spider_args=self.spider_args,
                crawl_response=crawl_response,
                metrics=metrics)
            return rv

        spider = spider_class()

        crawl_start_time = datetime.datetime.utcnow()
        crawl_response = spider.walk(*self.spider_args)
        crawl_end_time = datetime.datetime.utcnow()

        self._add_timing_entry_to_metrics_dict(
            metrics,
            crawl_start_time,
            crawl_end_time,
            "crawl")

        crawl_response = CrawlResponse(
            uuid=self.uuid,
            spider_name=self.spider_name,
            spider_args=self.spider_args,
            crawl_response=crawl_response,
            metrics=metrics)

        return crawl_response

    def _add_timing_entry_to_metrics_dict(
        self,
        metrics,
        start_time,
        end_time,
        key_prefix):

        """process() collects a bunch of timing information during
        its execution. This method creates metrics from this raw information
        and adds those metrics to a dict which can be incorporated into
        the crawl response as timing/performance info."""

        # start time date in RFC 2822 format (same value as Date HTTP header)
        # ex "Thu, 28 Jun 2001 14:17:15 +0000"
        date_fmt = "%a, %d %b %Y %H:%M:%S +0000"
        start_time_key = "%s_start_time" % key_prefix
        metrics[start_time_key] = start_time.strftime(date_fmt)

        duration = end_time - start_time
        duration_in_seconds = round(duration.total_seconds(), 2)
        duration_key = "%s_time_in_seconds" % key_prefix
        metrics[duration_key] = duration_in_seconds


class CrawlResponseQueue(Queue):
    """After a :py:class:`clf.spider_host.CrawlRequest` is processed by a spider host,
    the spider host creates an instance of :py:class:`clf.spider_host.CrawlResponse`
    in response to the request and adds the :py:class:`clf.spider_host.CrawlResponse`
    to a :py:class:`clf.spider_host.CrawlResponseQueue`."""

    @classmethod
    def get_message_class(cls):
        return CrawlResponse

    @classmethod
    def get_queue_name_prefix(cls):
        return "clf_cres_"


class CrawlResponse(Message):

    @classmethod
    def get_schema(cls):
        additional_properties = {
            "spider_name": {
                "type": "string",
                "minLength": 1,
            },
            "spider_args": {
                "type": "array",
                "items": {
                    "type": "string",
                    "minLength": 1,
                },
            },
            "crawl_response": {
                "type": "object",
            },
            "metrics": {
                "type": "object",
            },
        }

        required_properties = [
            "spider_name",
            "spider_args",
            "crawl_response",
            "metrics",
        ]

        rv = Message.get_schema(additional_properties, required_properties)
        return rv
