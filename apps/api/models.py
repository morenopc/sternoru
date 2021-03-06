# -*- coding: UTF8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Profile(models.Model):
    user=models.ForeignKey(User,unique=True,verbose_name=_('user'))
    sex=models.PositiveSmallIntegerField(_('gender'),choices=((1,'M'),(0,'F')),default=1)

class Place(models.Model):
    name=models.CharField(_('name'), max_length=64)
    lat=models.FloatField(_('latitude'))
    lng=models.FloatField(_('longitude'))
    address=models.CharField(_('address'), max_length=64)

class Checkin(models.Model):
    profile=models.ForeignKey(Profile,verbose_name=_('user profile'))
    place=models.ForeignKey(Place,verbose_name=_('place'))
    time=models.DateTimeField(_('alterado em'), auto_now=True)

