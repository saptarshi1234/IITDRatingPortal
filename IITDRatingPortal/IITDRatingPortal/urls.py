"""IITDRatingPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import _thread
import time
from datetime import datetime, timezone, timedelta

from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('',include('root.urls')),
    url(r'^users/',include('users.urls')),
    url(r'^professors/',include('professors.urls')),
    url(r'^courses/',include('courses.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    url(r'^allauth/', include('allauth.urls')),
]


def back():
    while True:
        for user in User.objects.all():
            profile = user.userprofile
            if user.userprofile.is_banned:
                # print(datetime.now(timezone.utc) - profile.banned_on - timedelta(seconds=profile.ban_days))
                # print(datetime.now(timezone.utc) - profile.banned_on > timedelta(seconds=profile.ban_days))
                # print(profile.indefinite_ban)
                if (not profile.indefinite_ban) and datetime.now(timezone.utc) - profile.banned_on > timedelta(
                        days=profile.ban_days):
                    user.is_active = True
                    profile.is_banned = False
                    user.save()
                    # print('done')
        time.sleep(10000)


print('starting')
try:
    _thread.start_new_thread(back, ())
except:
    print('error')
