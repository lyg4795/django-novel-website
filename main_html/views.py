from django.shortcuts import render
import os
from .models import book,readed
from django.http import HttpResponseRedirect
from main_html.tasks import findbook,add
def main_view(req):
    username=None
    if req.user.username!=None:
        username=req.user.username
    # 当没有登录时候会出错
    try:
        r = readed.objects.all().filter(reader=req.user)
    except:
        r = []
    books = book.objects.all().order_by('?')[:9]
    # 增加模糊搜索功能，显示满足关键字的全部书
    search=req.GET.get('search')
    if (search!='')&(search is not None):
        books = book.objects.all().filter(name__contains=search)
    if books.count() == 0:
        findbook.delay(search)
        # add.delay()
        return render(req, 'redirect.html', {'title': '书不存在', 'status': "正在通过爬虫获取，请稍后再试"})
    context={
        'books': books,
        'username': username,
        'readed':r
    }
    return render(req,'main.html',context=context)
def index(req,slug):
    books=book.objects.all().filter(name=slug)
    basedir = os.path.dirname(__file__)
    book_index=os.listdir(basedir+'/static/'+books.first().index)
    book_index.sort(key=lambda x:int(x[:-4]))
    chapter=[]
    for ind in book_index:
        with open(basedir+'/static/my/book/'+books.first().name+'/index/'+ind)as f:
            chapter.append(f.readline())
    context={
        'author':books.first().author,
        'name':books.first().name,
        'img':books.first().img,
        'describe':books.first().describe,
        'test':zip(book_index,chapter)

    }
    return render(req,'index.html',
                  context=context
                  )
def content(req,content,slug):
    basedir = os.path.dirname(__file__)+'/static/my/book/'+content+'/index/'+slug
    readed=[]
    with open(basedir)as f:
        chapter=f.readline()
        for r in f.readlines():
            for s in r.split('　　'):
                readed.append('　　'+s)
    number=int(slug[:-4])
    context={
        'content':readed,
        'chapter':chapter,
        'next':str(number+1)+'.txt',
        'above':str(number-1)+'.txt',
        'index':'/'+content
    }
    return render(req,'content.html',context=context)
def delete_record(req):
    username = None
    if req.user.username != None:
        username = req.user.username
    # 当没有登录时候会出错
    try:
        r = readed.objects.all().filter(reader=req.user)
    except:
        r = []
    r.delete()
    return render(req,'delete_record.html',{'readed':r})
# Create your views here.
