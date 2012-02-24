#!/usr/bin/python
# -*- coding: UTF8 -*-

#from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
#from django.core import serializers
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from api.models import Profile, Place, Checkin
from api.haversine import dec_distance
from django.core import serializers
import math
import datetime
from django.db.models import Count
#from api.forms import PesqForm

#
# 1. places
#
# Query to
# Get a list of places (DB model Place) around user's current location if lat/lng specified,
# otherwise all places.
#
def places(request):
    json=[]
    limit=10
    offset=0
    distance=None
    data=[]
    
    if request.method == 'GET':
        
        try:
            limit=int(request.GET.get('limit'))
            offset=int(request.GET.get('offset'))
        except:
            pass
        
        # Query
        # SELECT id, ( 3959 * acos( cos( radians(37) ) * cos( radians( lat ) ) * cos( radians( lng ) - radians(-122) ) + sin( radians(37) ) * sin( radians( lat ) ) ) ) AS distance FROM markers HAVING distance < 25 ORDER BY distance LIMIT 0 , 20;
        #
        # @@@ The best solution is with GeoDjango        
        #
        queryset=Place.objects.all() 
        try:
            lat=float(request.GET.get('lat'))
            lng=float(request.GET.get('lng'))
            
            for qs in queryset:
                distance=dec_distance(lng,lat,qs.lng,qs.lat)
                distance=round(distance,3)
                distance*=1000# convert to meters
                #if distance < 40:
                data+=[{"id":int(qs.id),"name":qs.name,"lat":str(qs.lat),"lng":str(qs.lng),"address":qs.address,"distance":int(distance)}]
            
            data=sorted(data, key=lambda tup: tup['distance'])
            
        except:
            for qs in queryset:
                data+=[{"id":int(qs.id),"name":qs.name,"lat":str(qs.lat),"lng":str(qs.lng),"address":qs.address,"distance":distance}]
        
        data=data[offset:limit]
        
        json={"response":{"meta":{"limit":int(limit),"offset":int(offset),"sort":"-distance","count":int(queryset.count())},
            "errors":[{"def":"1.places"}],
            "data":data
            }
        }
        
    return HttpResponse(json.values(), mimetype="application/json")

#
# 2. places details
# Details for a single place (DB model Place). Includes nested Check-ins in the response.
# /api/v1/places/1003?lat=55.748223&lng=37.587366
#
def places_details(request,places_id):
    
    json=[]
    checkins=[]
    distance=None
    
    if request.method == 'GET':

        place=get_object_or_404(Place, pk=places_id)
        qs_checkins=Checkin.objects.filter(place=place.id).order_by('-time')
        # time "2 hours ago"
        for qs in qs_checkins[:3]:
            checkins+=[{"id":int(qs.id),"time":qs.time.strftime('%I:%m:%S%p'),"user":{"id":qs.profile.user.id,"username":qs.profile.user.username}}]
        
        try:
            lat=float(request.GET.get('lat'))
            lng=float(request.GET.get('lng'))
            
            distance=dec_distance(lng,lat,place.lng,place.lat)
            distance=round(distance,3)
            distance*=1000# convert to meters
            
        except:
            pass
            
        json={"response":{"meta":{},
            "errors":[{"def":"2.places default"}],
            "data":[{"id":place.id,"name":place.name,"lat":str(place.lat),"lng":str(place.lng),"address":place.address,"distance":distance,"checkins_count":qs_checkins.count(),
            "checkins":checkins
                    }]
                }
            }
    return HttpResponse(json.values(), mimetype="application/json")
    
#
# 3. Place check-ins (list)
# Get a list of Check-ins for a specific Place.
# /api/v1/places/1003/checkins?limit=10&offset=0
#
def checkins_list(request,places_id):
    
    json=[]
    checkins=[]
    limit=10
    offset=0
    
    if request.method == 'GET':
        try:
            limit=int(request.GET.get('limit'))
            offset=int(request.GET.get('offset'))
        except:
            pass
        
        qs_checkins=Checkin.objects.filter(place=places_id).order_by('-time')[offset:limit]
        # time "2 hours ago"
        for qs in qs_checkins[:3]:
            checkins+=[{"id":int(qs.id),"time":qs.time.strftime('%I:%m:%S%p'),"user":{"id":qs.profile.user.id,"username":qs.profile.user.username}}]
     
    json={"response":{"meta":{},
            "errors":[{"def":"3. Place check-ins (list)"}],
            "data":{
            "checkins":checkins
                    }
                }
            }
    return HttpResponse(json.values(), mimetype="application/json")

#
# 4. Place check-in (action)
# Creates a Check-in in a Place by a currently logged in User.
#
def checkin(request,places_id):
    
    json=[]
    status="error"
    checkin=[]
    
    if request.method == 'GET':
        
        profile=get_object_or_404(Profile,user=request.user.id)
        place=get_object_or_404(Place, pk=places_id)
        
        try:
            new_checkin=Checkin()
            new_checkin.profile=profile
            new_checkin.place=place
            new_checkin.time=datetime.datetime.now()
            new_checkin.save()
            status="success"
        
            checkin=[{"id":new_checkin.id,"time":new_checkin.time.strftime('%I:%m:%S%p'),"user":{"id":new_checkin.profile.user.id,"username":new_checkin.profile.user.username}}]
        
        except:
            pass
        
        json={"response":{"meta":{},
            "errors":[{"def":"4. Place check-in"}],
            "status":status,
            "data":{
                "checkin":checkin
                }
            }
        }
        
    return HttpResponse(json.values(), mimetype="application/json")

#
# 5. Users (list)
# Get a list of Users.
# /api/v1/users?limit=10&offset=0
#
def users_list(request):
    json=[]
    data=[]
    limit=10
    offset=0
    
    if request.method == 'GET':
        try:
            limit=int(request.GET.get('limit'))
            offset=int(request.GET.get('offset'))
        except:
            pass
        
        qs_profiles=Profile.objects.annotate(ckins=Count('checkin')).order_by('-ckins')[offset:limit]
        count=1
        for qs in qs_profiles:
            data+=[{"id":int(qs.id),"rank":count,"username":qs.user.username,"checkins":qs.ckins}]
            count+=1
            
        json={"response":{"meta":{
                                "limit":limit,
                                "offset":offset,
                                "sort":"rank",
                                "count":qs_profiles.count()},
            "errors":[{"def":"5. Users (list)"}],
            "data":data
            }
        }
        
    return HttpResponse(json.values(), mimetype="application/json")

#
# 6. User profile (single object)
# Get specific User profile details.
# /api/v1/users/1
#
def user(request,user_id):
    
    json=[]
    data=[]
    
    if request.method == 'GET':
        
        qs_profiles=Profile.objects.annotate(ckins=Count('checkin')).order_by('-ckins')
        #count=1
        #for qs in qs_profiles:
        #    data+=[{"id":int(qs.id),"rank":count,"username":qs.user.username,"checkins":qs.ckins}]
        #    count+=1
        
        profile=get_object_or_404(qs_profiles,pk=user_id)
        json={"response":{"meta":{},
            "errors":[{"def":"6. User profile (single object)"}],
            "data":[{"id":profile.id,"username":profile.user.username,"screenname":profile.user.get_full_name(),"rank":0,"checkins_count":profile.ckins}]
            }
        }
        
    return HttpResponse(json.values(), mimetype="application/json")

