from celery_update_novel import update

import os,sys,django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my.settings")
django.setup()

from main_html.models import book

# books = book.objects.all()
# for b in books:
#    update.delay(b.name)
update.delay('魔鬼传奇')
update.delay('黎明之剑')