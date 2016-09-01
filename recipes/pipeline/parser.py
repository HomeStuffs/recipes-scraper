class ParseRecipe(object):

    # Checks for invalid recipes
    def process_item(self, item, spider):

        if not item['url']:
            raise DropItem("Missing url in %s" % item)

        if not item['recipe_name']:
            raise DropItem("Missing recipe name in %s" % item)

        if not item['ingredients']:
            raise DropItem("Missing ingredients in %s" % item)

        return item
