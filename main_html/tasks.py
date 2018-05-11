# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from spider.find_book import find_book

@shared_task
def add():
    a=None
    if a:
        return 1
    else:
        return 2


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def findbook(bookename):
    find_book(bookename)