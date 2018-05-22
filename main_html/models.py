from django.db import models
from django.contrib.auth.models import User
class author(models.Model):
    def __str__(self):
        return self.name
    name=models.CharField(max_length=20)
class book(models.Model):
    def __str__(self):
        return self.name
    name=models.CharField(max_length=20)
    author=models.ForeignKey(author,on_delete=models.CASCADE)
    describe=models.TextField()
    index=models.CharField(max_length=100)
    img=models.CharField(max_length=100,default='')
class readed(models.Model):
    def __str__(self):
        return self.name
    name=models.CharField(max_length=100)
    reader=models.ForeignKey(User,on_delete=models.CASCADE)
class download(models.Model):
    def __str__(self):
        return self.name.name
    name=models.ForeignKey(book,on_delete=models.CASCADE)
    book_list=models.TextField()
# Create your models here.
