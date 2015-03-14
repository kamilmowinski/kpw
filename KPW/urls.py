from django.conf.urls import patterns, include, url
from django.contrib import admin

from KPW.views import HomePage, SearchView

urlpatterns = patterns('',
    url(r'^$', HomePage.as_view(), name='home'),
    url(r'^search$', SearchView.as_view(), name='search'),
    url(r'^admin/', include(admin.site.urls)),
)
