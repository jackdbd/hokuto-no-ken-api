# -*- coding: utf-8 -*-
"""Scrapy global settings.

See Also:
    https://doc.scrapy.org/en/latest/topics/settings.html
    https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
    https://doc.scrapy.org/en/latest/topics/spider-middleware.html
"""
import datetime
import os

tz = datetime.datetime.utcnow().astimezone().tzinfo
now = datetime.datetime.now(tz)
started_at = f"{now.year}-{now.month}-{now.day}_{now.hour}-{now.minute}-{now.second}"

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# https://doc.scrapy.org/en/latest/topics/settings.html#bot-name
BOT_NAME = os.path.split(HERE)[1]

# Crawl responsibly by identifying yourself on the user-agent.
# https://doc.scrapy.org/en/latest/topics/settings.html#user-agent
# https://developers.google.com/search/reference/robots_txt
USER_AGENT = f"{BOT_NAME}(+https://github.com/jackdbd/hokuto-no-ken-api)"

# Obey robots.txt rules.
# https://doc.scrapy.org/en/latest/topics/settings.html#robotstxt-obey
# https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#topics-dlmw-robots
ROBOTSTXT_OBEY = True

# https://doc.scrapy.org/en/latest/topics/settings.html#std:setting-SPIDER_MODULES
SPIDER_MODULES = [f"{BOT_NAME}.spiders"]
# https://doc.scrapy.org/en/latest/topics/settings.html#newspider-module
NEWSPIDER_MODULE = f"{BOT_NAME}.spiders"

# https://doc.scrapy.org/en/latest/topics/settings.html#concurrent-requests
CONCURRENT_REQUESTS = 16

# https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# The DOWNLOAD_DELAY setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16
# See also autothrottle settings and docs.
DOWNLOAD_DELAY = 0.25

# https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#cookies-enabled
COOKIES_ENABLED = True

# https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#std:setting-COOKIES_DEBUG
COOKIES_DEBUG = True

# https://doc.scrapy.org/en/latest/topics/telnetconsole.html#topics-telnetconsole
TELNETCONSOLE_ENABLED = False

# https://doc.scrapy.org/en/latest/topics/settings.html#default-request-headers
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    f"{BOT_NAME}.middlewares.HokutoSpiderMiddleware": 543,
# }

# https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    f"{BOT_NAME}.middlewares.HokutoDownloaderMiddleware": 543,
# }

# I don't need the TelnetConsole, so I disable it.
# https://docs.scrapy.org/en/latest/topics/extensions.html#disabling-an-extension
# Keep in mind that quite a few Scrapy extensions are enabled by default.
# https://doc.scrapy.org/en/latest/topics/settings.html#extensions-base
EXTENSIONS = {
   'scrapy.extensions.telnet.TelnetConsole': None,
}

# I don't configure Feed Exports because I store the scraped data in Redis with
# scrapy_redis.pipelines.RedisPipeline and optionally in a JSON Lines via the -o
# flag passed to the scrapy crawl CLI.
# https://docs.scrapy.org/en/latest/topics/feed-exports.html
# https://docs.scrapy.org/en/latest/topics/commands.html#std:command-crawl

# I think it's better to define ITEM_PIPELINES in a spider's custom_settings
# instead of defining them globally here. Different spiders might need to send
# the scraped items to different pipelines.
# https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {}

# AutoThrottle might be quite useful to crawl some websites. I don't think I
# really need it for this project though, so I leave it disabled.
# https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = False

# HTTP caching would probably make the spiders harder to debug. Since there are
# no performance requirements for this project, I simply don't use it.
# https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = False

# I think it's useful to see which requests are duplicated, so I log them.
# https://docs.scrapy.org/en/latest/topics/settings.html#dupefilter-class
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
DUPEFILTER_DEBUG = True

# https://docs.scrapy.org/en/latest/topics/settings.html#scheduler
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# https://doc.scrapy.org/en/latest/topics/settings.html#log-level
LOG_LEVEL = "DEBUG"
LOG_FILE = f"{started_at}_{BOT_NAME}.log"
