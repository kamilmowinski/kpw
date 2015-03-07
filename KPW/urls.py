from django.conf.urls import patterns, include, url
from django.contrib import admin

from KPW.views import HomePage

urlpatterns = patterns('',
    url(r'^$', HomePage.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
)
