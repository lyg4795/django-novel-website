from find_book import find_book
from test import add
from celery import Celery
celery = Celery('celery_update_novel')

@celery.task
def update(bookname):
    find_book(bookname)
    # return add()
# update()
# import time
# from celery import Celery
# celery = Celery('celery_update_novel')
#
# @celery.task
# def sendmail(mail):
#     print('sending mail to'+mail)
#     time.sleep(2.0)
#     print('mail sent.')