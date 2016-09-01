# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecipesItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    url = scrapy.Field()
    recipe_name = scrapy.Field()
    ingredients = scrapy.Field()
    review_count = scrapy.Field()
    rating = scrapy.Field()
    rating_scale = scrapy.Field()
