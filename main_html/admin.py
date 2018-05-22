from django.contrib import admin
from .models import author,book,readed,download
admin.site.register(author)
admin.site.register(book)
admin.site.register(readed)
admin.site.register(download)
# Register your models here.
