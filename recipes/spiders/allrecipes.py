import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

import hashlib
import re

from recipes.spiders.extractors.allrecipes.extractor import parse_ingredient
from recipes.items import RecipesItem

class AllRecipesSpider(scrapy.spiders.CrawlSpider):
    name = "allrecipes"
    allowed_domains = ["allrecipes.com"]
    start_urls = [
        "http://allrecipes.com/recipes/"
    ]

    rules = (
        Rule(LinkExtractor(allow=".*", deny="/recipe/[0-9]+/[a-z\-]+/$"), follow=True),
        Rule(LinkExtractor(allow="/recipe/[0-9]+/[a-z\-]+/$"), follow=True, callback='parse_recipe')
    )

    scraped_item_count = 0

    def parse_recipe(self, response):

        # Extract the url
        url = response.url
        title_text = response.xpath('//title/text()').extract()[0]


        # Extract the recipe title
        title_suffix = ' - Allrecipes.com'
        title_text = response.xpath('/html/head/title/text()').extract()[0]
        recipe_name = title_text
        if recipe_name.endswith(title_suffix):
            recipe_name = recipe_name[:-len(title_suffix)]

        # Extract the ingredients
        ingredient_text = response.xpath("//span[@class='recipe-ingred_txt added'][@itemprop='ingredients']/text()").extract()
        ingredients = map(parse_ingredient, ingredient_text)

        # Id is based on the url
        recordId = hashlib.md5(url).hexdigest()

        rating_text = response.xpath("//section[@class='recipe-summary clearfix']//meta[@property='og:rating']/@content").extract()
        if not rating_text:
            rating_text = response.xpath("//section[@class='recipe-summary downsized clearfix']//meta[@property='og:rating']/@content").extract()
        rating = rating_text

        rating_scale_text = response.xpath("//section[@class='recipe-summary clearfix']//meta[@property='og:rating_scale']/@content").extract()
        if not rating_scale_text:
            rating_scale_text = response.xpath("//section[@class='recipe-summary downsized clearfix']//meta[@property='og:rating_scale']/@content").extract()
        rating_scale = rating_scale_text

        review_count_text = response.xpath("//div[@class='total-made-it']//span[@class='review-count']/text()").extract()
        review_count = re.match('^(\d+)', review_count_text[0])

        recipe = RecipesItem();
        recipe['id'] = recordId
        recipe['url'] = url
        recipe['recipe_name'] = recipe_name
        recipe['ingredients'] = ingredients

        if rating:
            recipe['rating'] = rating

        if rating_scale:
            recipe['rating_scale'] = rating_scale

        if review_count:
            recipe['review_count'] = review_count.group(0)

        AllRecipesSpider.scraped_item_count += 1
        self.logger.info(recipe)
        self.logger.info("Found recipe :" + str(AllRecipesSpider.scraped_item_count))

        yield recipe
