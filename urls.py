from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #(r'^$', login_required(direct_to_template), {'template': 'home.html'}),
    (r'^api/', include('api.urls', namespace='api')),
    
    url(r'^admin/', include(admin.site.urls)),
)
