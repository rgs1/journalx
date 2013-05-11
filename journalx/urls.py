from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^entries/$', 'entries_svc.views.index'),
    url(r'^admin/', include(admin.site.urls)),
)
