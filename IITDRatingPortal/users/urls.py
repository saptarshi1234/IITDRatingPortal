from django.conf.urls import url, include
from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^$', views.UserFormView.as_view(), name='sign_in'),
    url(r'profile$', views.show_user_profile, name='show_profile'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('accounts/', include('django.contrib.auth.urls')),

]
