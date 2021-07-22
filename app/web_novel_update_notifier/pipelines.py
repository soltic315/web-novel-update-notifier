# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from web_novel_update_notifier.lib.slack_webhook import SlackWebhook
from web_novel_update_notifier.lib.novel_table_manager import NovelTableManager


class WebNovelUpdateNotifierPipeline(object):
    def __init__(self, settings, *args, **kwargs):
        super(WebNovelUpdateNotifierPipeline, self).__init__(*args, **kwargs)

        self.novel_table = NovelTableManager()

        self.slack_webhook = SlackWebhook(
            slack_url=settings.get('SLACK_URL'),
            slack_channel=settings.get('SLACK_CHANNEL'),
            slack_bot_name=settings.get('SLACK_BOT_NAME'),
            slack_bot_icon=settings.get('SLACK_BOT_ICON'),
        )

    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings)

    def process_item(self, item, spider):
        if self.novel_table.novel_exists(item):
            if self.novel_table.is_novel_updated(item):
                self.novel_table.update_novel(item)
                self.slack_webhook.post_novel(item)
        else:
            self.novel_table.insert_novel(item)

        return item
