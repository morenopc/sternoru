#!/usr/bin/python
# -*- coding: UTF8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('api.views',
    url(r'^v1/places','places',name='places'),
    url(r'^v1/places/(\d+)','places_details',name='places_details'),
    url(r'^v1/places/(\d+)/checkin$','checkin',name='checkin'),
    url(r'^v1/places/(\d+)/checkins','checkins_list',name='checkins_list'),
    url(r'^v1/users/(\d+)$','user',name='user'),
    url(r'^v1/users','users_list',name='users_list'),
)
