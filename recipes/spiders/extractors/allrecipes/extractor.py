import re

words = []
with open("recipes/spiders/data/quantity_words.txt") as f:
    for line in f.readlines():
        words.append(line.strip())
print words

def parse_ingredient(ing):
    recipe_ingredient = {}

    quantity, ing = extract_quantity(ing)
    if (quantity): recipe_ingredient['quantity'] = quantity

    ing = scrape_alt_quantity(ing, recipe_ingredient)

    measurement, ing = extract_measurement(ing)
    if (measurement): recipe_ingredient['measurement'] = measurement

    ing = scrape_alt_quantity(ing, recipe_ingredient)


    ingredient, optional = extract_ingredient(ing)
    if ingredient: recipe_ingredient['ingredient'] = ingredient
    if optional: recipe_ingredient['optional'] = True

    return recipe_ingredient

def scrape_alt_quantity(ing, recipe_ingredient, replace=True):
    alternate = re.match('^\([A-za-z0-9\s\.]+\)', ing)
    if alternate is not None:
        if replace: ing = ing.replace(alternate.group(0), "")
        alt = alternate.group(0)[1:-1]  # strip parenthesis

        alt_quantity, alt = extract_quantity(alt)
        if (alt_quantity): recipe_ingredient['alt_quantity'] = alt_quantity
        alt_measurement, alt = extract_measurement(alt)
        if (alt_measurement): recipe_ingredient['alt_measurement'] = alt_measurement
    return ing.strip()

def extract_quantity(ing, replace=True):
    quantityResult = re.match('^[0-9/\.\s]+\s*', ing)
    if quantityResult is not None:
        quantity = quantityResult.group(0)
        if replace: ing = ing.replace(quantity, '').strip()
        return quantity.strip(), ing
    return "", ing

def extract_measurement(ing, replace=True):
    bestWord = ""
    replacement = ""
    for word in words:
        regex = '^' + word + '\s*'
        measurementResult = re.match(regex, ing)
        if measurementResult is not None:
            if (len(word) > len(bestWord)):
                bestWord = word
                replacement = measurementResult.group(0)

    if replace and replacement: ing = ing.replace(replacement, '').strip()

    return bestWord, ing

def extract_ingredient(ing):
    optional = False
    ingredient = ing

    optional_str = "(optional)"
    if (ingredient.endswith(optional_str)):
        optional = True
        ingredient = ingredient.replace(optional_str, "")

    return ingredient.strip(), optional
