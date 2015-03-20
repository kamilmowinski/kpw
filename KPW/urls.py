from django.conf.urls import patterns, include, url
from django.contrib import admin

from KPW.views import HomePage, SearchView, RedirectView

urlpatterns = patterns('',
    url(r'^$', HomePage.as_view(), name='home'),
    url(r'^search$', SearchView.as_view(), name='search'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^r/(?P<url>.+)$', RedirectView.as_view(), name='redirect'),
)
