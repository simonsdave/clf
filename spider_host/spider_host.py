#!/usr/bin/env python
"""This module is the spider host's mainline."""

import logging

from dasutils import tsh
from dasutils.rrsleeper import RRSleeper

from clparser import CommandLineParser
import mainloop
from clf.queues import CrawlRequestQueue
from clf.queues import CrawlResponseQueue


_logger = logging.getLogger("CLF_%s" % __name__)


if __name__ == "__main__":
    tsh.install()

    clp = CommandLineParser()
    (clo, cla) = clp.parse_args()

    logging.basicConfig(level=clo.logging_level)

    fmt = (
        "Spider Host "
        "reading requests from queue '{clo.request_queue_name}', "
        "writing responses to queue '{clo.response_queue_name}' "
        "and sleeping {clo.min_num_secs_to_sleep} to "
        "{clo.max_num_secs_to_sleep} seconds"
    )
    _logger.info(fmt.format(clo=clo))

    request_queue = CrawlRequestQueue.get_queue(clo.request_queue_name)
    if not request_queue:
        _logger.error(
            "Could not find request queue '%s'",
            clo.request_queue_name)
        sys.exit(1)

    response_queue = CrawlResponseQueue.get_queue(clo.response_queue_name)
    if not response_queue:
        _logger.error(
            "Could not find response queue '%s'",
            clo.response_queue_name)
        sys.exit(1)

    rrsleeper = RRSleeper(clo.min_num_secs_to_sleep, clo.max_num_secs_to_sleep)

    mainloop.run(request_queue, response_queue, rrsleeper)
