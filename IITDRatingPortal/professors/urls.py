from django.conf.urls import url
from . import views

app_name = 'professors'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'add_review$', views.ProfRatingCreate.as_view(), name='add_rating'),
    url(r'(?P<pk>[0-9]+)/delete_prof_review$', views.ProfRatingDelete.as_view(), name='delete_rating'),

]
