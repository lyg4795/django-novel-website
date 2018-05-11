
import requests
from urllib.parse import quote
import scrapy
import sys
# 设置django环境，不然无法用model的方法将数据存入到数据库，会报错
# django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
import os,sys,django
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my.settings")
django.setup()

from main_html.models import book,author as author_model
def find_book(books):
    headers={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',

    }
    # quote用来url转码
    url='http://www.biquge.com.tw/modules/article/soshu.php?searchkey=+'+quote(books,encoding='gb2312')
    req=requests.get(url,headers=headers)
    def analyze(req):
        detail=req.content.decode('gbk')
        # 用的是scrapy的选择器
        selector=scrapy.Selector(text=detail)
        print('request success')

        img=selector.xpath('//div[@id="fmimg"]/img/@src').extract_first()
        bookname=selector.xpath('//div[@id="info"]/h1/text()').extract_first()
        author=selector.xpath('//div[@id="info"]/p/text()').extract_first()
        intro=selector.xpath('//div[@id="intro"]/p/text()').extract_first()
        if img is None:
            books=selector.xpath('//*[@id="nr"]')
            for b in books:
                url_analyze=b.xpath('.//a/@href').extract_first()
                req_analyze=requests.get(url_analyze,headers=headers)
                analyze(req_analyze)
            return "no book"

        imghtml=requests.get('http://www.biquge.com.tw/'+img)
        lists = selector.xpath('//div[@id="list"]//a/@href').extract()

        # 创建小说路径
        basedir=os.path.dirname(os.path.dirname(__file__))+'/main_html/static/my/book/'+bookname+'/'
        try:
            os.mkdir(basedir)
            os.mkdir(basedir+'index')
        except:
            pass
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

            # f.write(str(len(lists)))
        # 从上一次结束的章节作为起点开始爬
        # 增加try，防止中途连接出错等错误丢失count
        try:
            for li in lists[count:]:
                req=requests.get('http://www.biquge.com.tw'+li)
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
        # 存入当前的小说章节数目，作为下一次爬虫的起点
        with open(basedir + 'count.txt', 'w')as f1:
            f1.write(str(count))
        bookget=book.objects.filter(name=bookname)
        if not bookget:
            # 存入作者
            a=author_model.objects.create(name=author)
            a.save()
            # 存入书本
            b=book.objects.create(name=bookname,author=a,index='my/book/'+bookname+'/index',
                                describe=intro,img='my/book/'+bookname+'/'+bookname+'.jpg')
            b.save()
            print('saved')
    analyze(req)
if __name__ == '__main__':
    books=book.objects.all()
    for b in books:
        find_book(b.name)
    # find_book('我是至尊')