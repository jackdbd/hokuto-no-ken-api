from scrapy import cmdline

SPIDER_NAME = "character"
cmdline.execute(f"scrapy crawl {SPIDER_NAME}".split())
# cmdline.execute(f"scrapy crawl {SPIDER_NAME} -o items.json -t json".split())
