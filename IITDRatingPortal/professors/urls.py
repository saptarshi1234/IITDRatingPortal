from django.conf.urls import url
from . import views

app_name = 'professors'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'add_review$', views.ProfRatingCreate.as_view(), name='add_rating'),
    url(r'rating/(?P<pk>[0-9]+)/delete_prof_review$', views.delete_rating, name='delete_rating'),
    url(r'rating/(?P<pk>[0-9]+)/upvote$', views.upvote, name='upvote'),
    url(r'rating/(?P<pk>[0-9]+)/downvote$', views.downvote, name='downvote'),

]
