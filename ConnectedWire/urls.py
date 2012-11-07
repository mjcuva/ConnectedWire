from django.conf.urls import patterns, include, url
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ConnectedWire.views.home', name='home'),
    # url(r'^ConnectedWire/', include('ConnectedWire.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^$', 'blog.views.index'),
    url(r'^.json/?(\d+)?/?$', 'blog.views.indexJson'),
    url(r'^login/?', 'blog.views.login'),
    url(r'^signup/?', 'blog.views.signup'),
    url(r'^logout/?', 'blog.views.logout'),
    url(r'^(\d+/\d+/\S+)/?', 'blog.views.permalink'),
    url(r'^newpost/?', 'blog.views.newpost'),
    url(r'^edit/(\d+)/?', 'blog.views.edit'),
    url(r'^edit/(\D+)/?', 'blog.views.pageEdit'),
    url(r'^category/(\D+)/?', 'blog.views.category'),
    url(r'^newpage/?', 'blog.views.newpage'),
    url(r'^(\d+)/?', 'blog.views.archive'),
    url(r'^search/?', 'blog.views.search'),
    url(r'^import/?', 'blog.import.importer'),
    url(r'^feed/?', 'blog.feed.feedBurn'),
    url(r'^dashboard/?', 'blog.dashboard.dash'),
    url(r'^(\D+)/?$', 'blog.views.page'),
    # url(r'^dbrequest.json$', 'blog.views.dbrequest')
    
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )