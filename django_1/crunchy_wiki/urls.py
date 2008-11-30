from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^crunchy_wiki/', include('crunchy_wiki.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^(?P<page_name>[^/]+)/$', 'crunchy_wiki.wiki.views.view_page'),
    (r'^(?P<page_name>[^/]+)/edit/$', 'crunchy_wiki.wiki.views.edit_page'),
    (r'^(?P<page_name>[^/]+)/save/$', 'crunchy_wiki.wiki.views.save_page'),
    (r'^(?P<page_name>[^/]+)/delete/$', 'crunchy_wiki.wiki.views.delete_page'),
    (r'^static/css/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/Users/andre/py-fun/django_1/crunchy_wiki/static/css/'}),
    (r'^static/images/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/Users/andre/py-fun/django_1/crunchy_wiki/static/images/'})
)
