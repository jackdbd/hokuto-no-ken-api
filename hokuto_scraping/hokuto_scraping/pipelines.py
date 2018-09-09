# -*- coding: utf-8 -*-
"""Item pipelines.

Don't forget to add your pipeline to the ITEM_PIPELINES setting (either in
settings.py on as custom_settings in one or more spiders.

Note: it seems that if you define ITEM_PIPELINES in a spider's custom_settings
property, any "global" item pipeline is NOT activated for that spider.

See Also
    https://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""
from scrapy.exceptions import DropItem


class DropItemPipeline(object):
    def process_item(self, item, spider):
        # TODO: maybe implement some logic to decide whether this item should
        # be sent to the next pipeline or dropped.
        if not item.get("is_valid", True):
            raise DropItem

        else:
            return item
