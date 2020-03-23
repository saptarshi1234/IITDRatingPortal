from django.conf.urls import url, include
from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^$', views.UserFormView.as_view(), name='sign_in'),
    url(r'profile$', views.show_user_profile, name='show_profile'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    url(r'(?P<user_id>[0-9]+)/ban_user/$', views.ban_user, name='ban_user'),

    # url(r'(?P<rating_id>[0-9]+)/ban_for_prof_review$',views.ban_user_prof_redirect,name='ban_user_prof_redirect'),
    # url(r'(?P<rating_id>[0-9]+)/ban_for_course_review$',views.ban_user_course_redirect,name='ban_user_prof_redirect'),
    url(r'(?P<user_id>[0-9]+)/remove_ban$',views.remove_ban,name='remove_ban'),

    path('accounts/', include('django.contrib.auth.urls')),

]
