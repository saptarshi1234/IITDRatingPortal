from django.conf.urls import url
from . import views

app_name = 'courses'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    url(r'(?P<pk>[0-9]+)/add_review$', views.CourseRatingCreate.as_view(), name='add_rating'),
    url(r'course_rating/(?P<pk>[0-9]+)/delete_course_review$', views.delete_rating, name='delete_rating'),
    url(r'course_rating/(?P<pk>[0-9]+)/report_course_review$', views.report_rating, name='report_rating'),
    url(r'course_rating/(?P<pk>[0-9]+)/unmark_rating$', views.unmark_rating, name='unmark_rating'),

    url(r'create_course$', views.CourseCreate.as_view(), name='create_course'),
    url(r'(?P<pk>[0-9]+)/update_course$', views.CourseUpdate.as_view(), name='update_course'),

    url(r'rating/(?P<pk>[0-9]+)/upvote$', views.upvote, name='upvote'),
    url(r'rating/(?P<pk>[0-9]+)/downvote$', views.downvote, name='downvote'),

]
