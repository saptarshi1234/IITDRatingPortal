from django.conf.urls import url
from . import views

app_name = 'professors'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    url(r'prof_rating/(?P<pk>[0-9]+)/delete_prof_review$', views.delete_rating, name='delete_rating'),
    url(r'prof_rating(?P<pk>[0-9]+)/report_prof_review$', views.report_rating, name='report_rating'),
    url(r'(?P<pk>[0-9]+)/add_review$', views.ProfRatingCreate.as_view(), name='add_rating'),
    url(r'prof_rating/(?P<pk>[0-9]+)/unmark_rating$', views.unmark_rating, name='unmark_rating'),

    url(r'create_prof$', views.ProfCreate.as_view(), name='create_prof'),
    url(r'(?P<pk>[0-9]+)/update_prof$', views.ProfUpdate.as_view(), name='update_prof'),

    url(r'rating/(?P<pk>[0-9]+)/upvote$', views.upvote, name='upvote'),
    url(r'rating/(?P<pk>[0-9]+)/downvote$', views.downvote, name='downvote'),

]
