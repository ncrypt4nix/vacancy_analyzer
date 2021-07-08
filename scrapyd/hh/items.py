import scrapy


class HHItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    wage = scrapy.Field()
    skills = scrapy.Field()
    url = scrapy.Field()
    experience = scrapy.Field()
    employment_mode = scrapy.Field()
    description = scrapy.Field()
