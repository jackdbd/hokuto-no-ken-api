# -*- coding: utf-8 -*-
"""Scrapy global settings.

For simplicity, this file contains only settings considered important or\
commonly used. You can find more settings consulting the documentation.

See Also
    https://doc.scrapy.org/en/latest/topics/settings.html
    https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
    https://doc.scrapy.org/en/latest/topics/spider-middleware.html
"""
import os

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

BOT_NAME = os.path.split(HERE)[1]

# Crawl responsibly by identifying yourself on the user-agent
# TODO: add user agent
USER_AGENT = f"{BOT_NAME}(+https://github.com/jackdbd/hokuto-no-ken-api)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

SPIDER_MODULES = [f"{BOT_NAME}.spiders"]
NEWSPIDER_MODULE = f"{BOT_NAME}.spiders"

# Maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Delay for requests on the same website (default: 0 seconds)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.25

# The DOWNLOAD_DELAY setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

COOKIES_ENABLED = True

TELNETCONSOLE_ENABLED = True

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    f"{BOT_NAME}.middlewares.HokutoSpiderMiddleware": 543,
# }

# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    f"{BOT_NAME}.middlewares.HokutoDownloaderMiddleware": 543,
# }

# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Feed Exports
# FEED_URI = f"file:///{ROOT}/export.jsonl"
# FEED_URI = "stdout:"
# FEED_FORMAT = "jsonlines"

# I think it's better to define ITEM_PIPELINES in a spider's custom_settings
# instead of defining them globally here. Different spiders might need to send
# the scraped items to different pipelines.
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {f"{BOT_NAME}.pipelines.DropItemPipeline": 100}

# AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# DUPEFILTER_DEBUG = True
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# SCHEDULER_PERSIST = True

LOG_LEVEL = "DEBUG"
