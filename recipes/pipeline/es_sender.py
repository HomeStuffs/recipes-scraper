import elasticsearch

from datetime import datetime
from elasticsearch import Elasticsearch
from scrapy.exceptions import DropItem

index_ = "scraped_recipes"
doc_type_ = "scraped"

class ElasticSearchSender(object):

    es = Elasticsearch([
        {'host': 'elasticsearch', 'port': 9200},
    ])

    custom_settings = {}

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        custom_settings = ElasticSearchSender.custom_settings
        custom_settings['index'] = settings['ELASTIC_SEARCH_INDEX']
        custom_settings['type'] = settings['ELASTIC_SEARC_TYPE']
        return cls()

    def process_item(self, item, spider):
        custom_settings = ElasticSearchSender.custom_settings

        body = {
            'timestamp': datetime.now(),
            'url': item['url'],
            'recipe_name': item['recipe_name'],
            'ingredients': item['ingredients'],
        }

        optional = ['review_count',
                    'rating',
                    'rating_scale']
        for o in optional:
            if o in item:
                body[o] = item[o]

        try:
            res = ElasticSearchSender.es.create(
                index = custom_settings['index'],
                doc_type = custom_settings['type'],
                body = body,
                id = item['id'],
            )
            spider.logger.info(res)
        except elasticsearch.ConflictError as e:
            res = ElasticSearchSender.es.update(
                index = custom_settings['index'],
                doc_type = custom_settings['type'],
                body = {'doc': body},
                id = item['id'],
            )
            spider.logger.info(res)

        return item
