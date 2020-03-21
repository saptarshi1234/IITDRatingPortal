from django.conf.urls import url,include
from django.urls import path

from . import views

app_name = 'root'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^search$', views.search, name='search'),

]
