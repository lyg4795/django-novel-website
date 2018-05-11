from  django.utils.deprecation import MiddlewareMixin
from main_html.models import readed
class ReadedMiddleware:
    def __init__(self,get_reponse):
        self.get_response=get_reponse
    def __call__(self, req):
        if req.user.username!='':
            if '.txt' in req.path:
                self.add_readed(req)
        # print(req.session)
        res=self.get_response(req)
        return res
    def add_readed(self,req):
        r=readed.objects.all()
        if r.count()<10:
            self.get(r,req)
        else:
            r.first().delete()
            self.get(r,req)
    def get(self,r,req):
        # 修改为书名相同时候的阅读记录只记录最新的那个
        rget=r.filter(name__contains=req.path.split('/')[1])
        if rget.count()==0:
            r.create(name=req.path, reader=req.user)
            # queryset has no attribute save() so I add [0] after r
            r[0].save()
        else:
            rget[0].delete()
            r.create(name=req.path, reader=req.user)
            # queryset has no attribute save() so I add [0] after r
            r[0].save()