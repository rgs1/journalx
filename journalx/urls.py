from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^entries/$', 'entries_svc.views.index'),
    url(r'^entries/(\d+)$', 'entries_svc.views.entry'),
    url(r'^entries/(\d+)/screenshot$', 'entries_svc.views.screenshot'),
    url(r'^entries/(\d+)/comments/$', 'entries_svc.views.comments_index'),
    url(r'^entries/(\d+)/comments/(\d+)$', 'entries_svc.views.comment'),
    url(r'^admin/', include(admin.site.urls)),
)
