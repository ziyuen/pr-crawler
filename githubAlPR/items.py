# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GithubalprItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    project_name = scrapy.Field()
    linked_issues = scrapy.Field()
    author_association = scrapy.Field()
    status = scrapy.Field()
    changed_files = scrapy.Field()
    additions = scrapy.Field()
    deletions = scrapy.Field()
    commits = scrapy.Field()
    comments = scrapy.Field()
    review_comments = scrapy.Field()
    time_span = scrapy.Field()
    
