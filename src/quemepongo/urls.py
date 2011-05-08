from django.conf.urls.defaults import patterns, include, url
import os.path
from settings import MEDIA_ROOT
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'quemepongo.views.home', name='home'),
    # url(r'^quemepongo/', include('quemepongo.foo.urls')),
    url(r'^recomendar/temperatura/', 'quemepongo.consejero.views.recomendar_temperatura'),
    url(r'^recomendar/localidad/', 'quemepongo.consejero.views.recomendar_localidad'),
    url(r'^$', 'quemepongo.consejero.views.recomendar_localidad', name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('django.views', (r'^images/(.*)$', 'static.serve', {'document_root': MEDIA_ROOT}), )
