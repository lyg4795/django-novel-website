from django.urls import path
from . import views
from my import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView
urlpatterns=[
    path('',views.main_view,name='main_view'),
    path('favicon.ico/',RedirectView.as_view(url='/static/my/favicon.ico')),
    path('<slug>/',views.index),
    path('<content>/<slug>',views.content),
    path('deleteRecord',views.delete_record)
]
urlpatterns+=static('/pic/', document_root=settings.MEDIA_ROOT)
