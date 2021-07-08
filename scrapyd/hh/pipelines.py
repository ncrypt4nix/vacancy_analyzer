import re
import json
import redis
import logging
from itemadapter import ItemAdapter

from hh import settings


logger = logging.getLogger()


class HhPipeline:
    class KeyNotFound(Exception):
        pass

    def open_spider(self, spider):
        self.reader = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            password=settings.REDIS_PASSWORD
        )

    def process_item(self, item, spider):
        item = self.normalize_item(item)
        try:
            key = self.get_key_to_reader(item)
            logger.info(f'Update redis key: {key}')
            self.reader.set(key, json.dumps(ItemAdapter(item).asdict()))
        except self.KeyNotFound:
            pass
        return item

    def get_key_to_reader(self, item):
        math = re.search(rf'{settings.MAIN_HH_DOMAIN}\/vacancy\/(\d+)', item['url'])
        if not math:
            raise self.KeyNotFound
        id = math.group(1)
        return '_'.join([settings.REDIS_PREFIX, id])

    def normalize_item(self, item):
        item['wage'] = item['wage'].replace(u'\xa0', u' ')
        return item
