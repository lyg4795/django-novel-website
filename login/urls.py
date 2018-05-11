from django.urls import path
from django.contrib.auth.views import login, logout
from . import views
urlpatterns=[
    path('registe',views.registe_view,name='registe'),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view)
]