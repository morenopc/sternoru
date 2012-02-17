# -*- coding: UTF8 -*-

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	user=models.ForeignKey(User,unique=True,verbose_name=_("user"))
    sex=models.PositiveSmallIntegerField(u'gender?',choices=((1,'M'),(0,'F')),default=1)

class Place(models.Model):
    name=models.CharField('name', max_length=64)
    lat=models.FloatField('latitude')
    lng=models.Floatield('longitude')
    address=models.CharField('address', max_length=64)

class Checkin(models.Model):
    profile=models.ForeignKey(Profile,unique=True,verbose_name=_("user profile"))
    place=models.ForeignKey(Place,unique=True,verbose_name=_("place"))
    time=models.DateTimeField('alterado em', auto_now=True)

