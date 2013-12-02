"""..."""

import logging

from clf.spider_repo.spider_repo import SpiderRepo


_logger = logging.getLogger("CLF_%s" % __name__)


command_name = "sr"


def doit(usage_func, args):

    if len(args) < 1:
        usage_func("%s [create|rm|ls|up] ..." % command_name)
        spider_repo_usage()

    commands = {
        "c": _create,
        "create": _create,
        "d": _delete,
        "rm": _delete,
        "del": _delete,
        "delete": _delete,
        "ls": _ls,
        "upload": _upload,
        "up": _upload,
        "u": _upload,
    }
    command = commands.get(args[0].strip().lower(), None)
    if not command:
        usage_func("%s [create|del|ls|up] ..." % command_name)

    command(usage_func, args[1:])


def _create(usage_func, args):
    if 1 != len(args):
        usage_func("%s create <repo-name>" % command_name)
    
    repo_name = args[0]

    spider_repo = SpiderRepo.get_repo(repo_name)
    if spider_repo:
        print "Spider repo '%s' already exists" % repo_name
    else:
        spider_repo = SpiderRepo.create_repo(repo_name)
        if spider_repo:
            print "Created spider repo '%s'" % spider_repo
        else:
            _logger.error("Could not create spider repo '%s'", repo_name)


def _delete(usage_func, args):
    if 1 != len(args):
        usage_func("%s delete <repo-name>" % command_name)

    repo_name = args[0]

    spider_repo = SpiderRepo.get_repo(repo_name)
    if spider_repo:
        spider_repo.delete()
        print "Deleted spider repo '%s'" % repo_name
    else:
        _logger.error("Could not find spider repo '%s'", repo_name)


def _ls(usage_func, args):
    if 1 < len(args):
        usage_func("%s ls [<repo-name>]" % command_name)

    if 0 == len(args):
        for spider_repo in SpiderRepo.get_all_repos():
            print spider_repo
    else:
        repo_name = args[0]

        spider_repo = SpiderRepo.get_repo(repo_name)
        if spider_repo:
            for spider in spider_repo.spiders():
                print "-- %s" % spider
        else:
            _logger.error("Could not find spider repo '%s'", repo_name)


def _upload(usage_func, args):
    if 2 != len(args):
        usage_func("%s up <repo-name> <spider-file-name>" % command_name)

    repo_name = args[0]
    spider_file_name = args[1]

    spider_repo = SpiderRepo.get_repo(repo_name)
    if spider_repo:
        if spider_repo.upload_spider(spider_file_name):
            fmt = "Success uploading '%s' to spider repo '%s'"
            _logger.info(fmt, spider_file_name, repo_name)
        else:
            fmt = "Failed to upload '%s' to spider repo '%s'"
            _logger.error(fmt, spider_file_name, repo_name)
    else:
        _logger.error("Could not find spider repo '%s'", repo_name)
