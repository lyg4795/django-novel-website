import pdb
import requests
from urllib.parse import quote
import scrapy
import json
import time
# 设置django环境，不然无法用model的方法将数据存入到数据库，会报错
# django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
import os,sys,django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my.settings")
django.setup()

from main_html.models import book,author as author_model,download


def find_book(books):
    headers={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',

    }
    # quote用来url转码
    # url='http://www.biquge5200.cc/modules/article/soshu.php?searchkey=+'+quote(books,encoding='gb2312')
    url = 'http://www.biquge5200.cc/modules/article/search.php?searchkey='+books
    req=requests.get(url,headers=headers)
    def analyze(req):
        detail=req.content.decode('gbk')
        # 用的是scrapy的选择器
        selector=scrapy.Selector(text=detail)
        print('request success')
        bookget = book.objects.filter(name='test')
        img=selector.xpath('//div[@id="fmimg"]/img/@src').extract_first()
        bookname=selector.xpath('//div[@id="info"]/h1/text()').extract_first()
        author=selector.xpath('//div[@id="info"]/p/text()').extract_first()
        intro=selector.xpath('//div[@id="intro"]/p/text()').extract_first()
        if img is None:
            books=selector.xpath('//table[@class="grid"]/tr')[1:]
            for b in books:
                url_analyze=b.xpath('.//a/@href').extract_first()
                req_analyze=requests.get(url_analyze,headers=headers)
                analyze(req_analyze)
            return "no book"

        imghtml=requests.get(img)
        lists = selector.xpath('//div[@id="list"]//a/@href').extract()

        # 创建小说路径
        basedir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/main_html/static/my/book/'+bookname+'/'
        try:
            os.makedirs(basedir+'index')
        except Exception as e:
            print(e)
        # 用于统计之前爬到了小说的第几个章节，用count计数
        try:
            with open(basedir+'count.txt')as f:
                count=int(f.readline())
        except:
            count=0
        # 保存图片
        with open(basedir+bookname+'.jpg','wb')as f:
            f.write(imghtml.content)
        # 保存信息
        with open(basedir+'info.txt','w')as f:
            f.write(author+'\n')
            f.write(intro+'\n')
        # for i in lists:
            
            # f.write(str(len(lists)))
        bookget = book.objects.filter(name=bookname)
        authorget=author_model.objects.filter(name=author)
        if not bookget:
            if not authorget:
                # 存入作者
                a=author_model.objects.create(name=author)
                a.save()
                authorget = author_model.objects.filter(name=author)
            # 存入书本
            b=book.objects.create(name=bookname,author=authorget[0],index='my/book/'+bookname+'/index',
                                describe=intro,img='my/book/'+bookname+'/'+bookname+'.jpg')
            b.save()
            bookget = book.objects.filter(name=bookname)
            print('saved {}'.format(bookname))
        book_list=download.objects.filter(name=bookget[0])
        if not book_list:
            d = download.objects.create(name=bookget[0], book_list='0')
            d.save()
            url_index=[]
        else:
            url_index=book_list[0].book_list.split(',')

        # 从上一次结束的章节作为起点开始爬
        # 增加try，防止中途连接出错等错误丢失count
        try:
            for li in lists[count+9:]:
                if not li in url_index:
                    time.sleep(0.5)
                    if len(url_index)<15:
                        url_index.append(li)
                    else:
                        url_index.pop(0)
                        url_index.append(li)
                    req=requests.get(li)
                    # d=download.objects.create(name=bookget[0],book_list=li)
                    # d.save()
                    selector=scrapy.Selector(text=req.content.decode('gbk','ignore'))
                    chapter_name=selector.xpath('//h1/text()').extract_first()
                    chapter_content=selector.xpath('//div[@id="content"]').xpath('string(.)').extract_first()
                    with open(basedir+'index/'+str(count)+'.txt','w')as f:
                        f.write(chapter_name+'\n')
                        f.write(chapter_content)
                    count+=1
                    print(count)

        except Exception as e:
            with open(basedir + 'info.txt', 'a')as f:
                f.write(str(e))

        book_list[0].book_list = ','.join(url_index)
        book_list[0].save()
        # 存入当前的小说章节数目，作为下一次爬虫的起点
        with open(basedir + 'count.txt', 'w')as f1:
            f1.write(str(count))
    analyze(req)
def update_novel():
    books = book.objects.all()
    for b in books:
       find_book(b.name)
if __name__ == '__main__':
    books=book.objects.all()
    #for b in books:
    #    find_book(b.name)
    find_book('黎明之剑')
