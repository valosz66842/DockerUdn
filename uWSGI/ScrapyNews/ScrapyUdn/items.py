# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from WebNews.models import Udn
class ScrapyudnItem(DjangoItem): #連結Django_model
    django_model = Udn
