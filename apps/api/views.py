#!/usr/bin/python
# -*- coding: UTF8 -*-

import math
import datetime
import json
from django.http import HttpResponse, HttpResponseRedirect
#from django.core import serializers
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from api.models import Profile, Place, Checkin
from api.haversine import dec_distance
from django.core import serializers
from django.db.models import Count
from django.http import Http404

#
# 1. places
#
# Query to
# Get a list of places (DB model Place) around user's current location if lat/lng specified,
# otherwise all places.
# 
#
def places(request):
    jn=[]
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
        # @@@ The best solution is with GeoDjango and Postgres   
        #
        queryset=Place.objects.all() 
        try:
            lat=float(request.GET.get('lat'))
            lng=float(request.GET.get('lng'))
            
            for qs in queryset:
                distance=dec_distance(lng,lat,qs.lng,qs.lat)
                distance=round(distance,3)
                if distance < 40:
                    data+=[{"id":int(qs.id),"name":qs.name,"lat":str(qs.lat),"lng":str(qs.lng),"address":qs.address,"distance":int(distance*1000)}]
            
            data=sorted(data, key=lambda tup: tup['distance'])
            
        except:
            for qs in queryset:
                data+=[{"id":int(qs.id),"name":qs.name,"lat":str(qs.lat),"lng":str(qs.lng),"address":qs.address,"distance":distance}]
        
        data=data[offset:limit]
        jn={"response":{"meta":{"limit":int(limit),"offset":int(offset),"sort":"-distance","count":int(queryset.count())},
            "errors":[],
            "data":data
            }
        }
        
    return HttpResponse(json.dumps(jn.values(),indent=4,separators=(',',':')), mimetype="application/json")

#
# 2. places details
# Details for a single place (DB model Place). Includes nested Check-ins in the response.
# /api/v1/places/1003?lat=55.748223&lng=37.587366
#
def places_details(request,places_id):
    
    jn=[]
    checkins=[]
    distance=None
    
    if request.method == 'GET':

        place=get_object_or_404(Place, pk=places_id)
        qs_checkins=Checkin.objects.filter(place=place.id).order_by('-time')
        # time "2 hours ago"
        for qs in qs_checkins[:3]:
            checkins+=[{"id":int(qs.id),"time":qs.time.strftime('%I:%M:%S%p'),"user":{"id":qs.profile.user.id,"username":qs.profile.user.username}}]
        try:
            lat=float(request.GET.get('lat'))
            lng=float(request.GET.get('lng'))
            
            distance=dec_distance(lng,lat,place.lng,place.lat)
            distance=round(distance,3)
            distance*=1000# convert to meters
            
        except:
            pass
            
        jn={"response":{"meta":{},
            "errors":[],
            "data":[{"id":place.id,"name":place.name,"lat":str(place.lat),"lng":str(place.lng),"address":place.address,"distance":int(distance),"checkins_count":qs_checkins.count(),
            "checkins":checkins
                    }]
                }
            }
    return HttpResponse(json.dumps(jn.values(),indent=4,separators=(',',':')), mimetype="application/json")
    
#
# 3. Place check-ins (list)
# Get a list of Check-ins for a specific Place.
# /api/v1/places/1/checkins?limit=10&offset=0
#
def checkins_list(request,places_id):
    
    jn=[]
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
            checkins+=[{"id":int(qs.id),"time":qs.time.strftime('%I:%M:%S%p'),"user":{"id":qs.profile.user.id,"username":qs.profile.user.username}}]
     
    jn={"response":{"meta":{},
            "errors":[],
            "data":{
            "checkins":checkins
                    }
                }
            }
    return HttpResponse(json.dumps(jn.values(),indent=4,separators=(',',':')), mimetype="application/json")

#
# 4. Place check-in (action)
# Creates a Check-in in a Place by a currently logged in User.
# /api/v1/places/1003/checkin
#
def checkin(request,places_id):
    
    jn=[]
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
        
            checkin=[{"id":int(new_checkin.id),"time":new_checkin.time.strftime('%I:%M:%S%p'),"user":{"id":new_checkin.profile.user.id,"username":new_checkin.profile.user.username}}]
        
        except:
            pass
        
        jn={"response":{"meta":{},
            "errors":[],
            "status":status,
            "data":{
                "checkin":checkin
                }
            }
        }
        
    return HttpResponse(json.dumps(jn.values(),indent=4,separators=(',',':')), mimetype="application/json")

#
# 5. Users (list)
# Get a list of Users.
# /api/v1/users?limit=10&offset=0
#
def users_list(request):
    jn=[]
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
        for rank, qs in enumerate(qs_profiles):
            data+=[{"id":int(qs.id),"rank":rank+1,"username":qs.user.username,"checkins":qs.ckins}]
            
        jn={"response":{"meta":{
                                "limit":limit,
                                "offset":offset,
                                "sort":"rank",
                                "count":qs_profiles.count()},
            "errors":[],
            "data":data
            }
        }
        
    return HttpResponse(json.dumps(jn.values(),indent=4,separators=(',',':')), mimetype="application/json")

#
# 6. User profile (single object)
# Get specific User profile details.
# /api/v1/users/1
#
def user(request,user_id):
    
    jn=[]
    data=[]
    
    if request.method == 'GET':
        
        try: 
            user_id=int(user_id)
        except:
            raise Http404
        
        qs_profiles=Profile.objects.annotate(ckins=Count('checkin')).order_by('-ckins')
        # not so good
        for pos, qs in enumerate(qs_profiles):
            if qs.id == user_id:
                rank=pos
        
        profile=get_object_or_404(qs_profiles,pk=user_id)
        jn={"response":{"meta":{},
            "errors":[],
            "data":[{"id":profile.id,"username":profile.user.username,"sex":profile.get_sex_display(),"rank":rank+1,"checkins_count":profile.ckins}]
            }
        }
        
    return HttpResponse(json.dumps(jn.values(),indent=4,separators=(',',':')), mimetype="application/json")

