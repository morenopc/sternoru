#!/usr/bin/python
# -*- coding: UTF8 -*-

#from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
#from django.core import serializers
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from api.models import Profile, Place, Checkin
from api.haversine import points2distance
from api.converter import dd2dms
from django.core import serializers
import math
#from api.forms import PesqForm

#
# 1. places
#
def places(request):
    json=[]
    limit=10
    offset=0
    distance=None
    data=[]
    
    if request.method == 'GET':
        
        # Query to
        # Get a list of places (DB model Place) around user's current location if lat/lng specified,
        # otherwise all places.
        
        try:
            limit=request.GET.get('limit')
            offset=request.GET.get('offset')
        except:
            pass
        
        #try:
        lat=request.GET.get('lat')
        lng=request.GET.get('lng')
        
        # Calcular raio
        queryset=Place.objects.all()[offset:limit]
        
        for qs in queryset:
            #distance=math.hypot(qs.lng-float(lng), qs.lat-float(lat))
            # converter os dois pontos para DMS
            dd2dms()
            # calcular a distancia entre eles em Km
            distance=points2distance([qs.lng,float(lng)], [qs.lat,float(lat)])
            print distance
            data+=[{"id":int(qs.id),"name":qs.name,"lat":str(qs.lat),"lng":str(qs.lng),"address":qs.address,"distance":distance}]
            
        #except:
        #    queryset=Place.objects.all()[offset:limit]
        #    
        #    for qs in queryset:
        #        data+=[{"id":int(qs.id),"name":qs.name,"lat":str(qs.lat),"lng":str(qs.lng),"address":qs.address,"distance":distance}]
        
        json={"response":{"meta":{"limit":int(limit),"offset":int(offset),"sort":"-distance","count":int(queryset.count())},
            "errors":[{"def":"1.places"}],
            "data":data
            }
        }
        
    return HttpResponse(json.values(), mimetype="application/json")

#
# 2. places details
#
def places_details(request,places_id):
    
    json=[]
    checkins=[]
    distance=None
    
    # Query to
    # Details for a single place (DB model Place). Includes nested Check-ins in the response.
    
    if request.method == 'GET':

        place=get_object_or_404(Place, pk=places_id)
        qs_checkins=Checkin.objects.filter(place=place.id)
        # calcular tempo "2 hours ago"
        for qs in qs_checkins:
            checkins+=[{"id":int(qs.id),"time":qs.time,"user":{"id":qs.profile.user.id,"username":qs.profile.user.username}}]
        
        try:
            json+=request.GET.get('lat')
            json+=request.GET.get('lng')
            # calcular distancia
        except:
            pass
        json={"response":{"meta":{},
            "errors":[],
            "data":[{"id":place.id,"name":place.name,"lat":str(place.lat),"lng":str(place.lng),"address":place.address,"distance":distance,"checkins_count":qs_checkins.count(),
            "checkins":checkins
                    }]
                }
            }
    #video=get_object_or_404(Musicas, video_id=video_id)
    return HttpResponse(json.values(), mimetype="application/json")
    
#
# Checkin
#
def checkin(request,places_id):
    json=places_id
    if request.method == 'GET':
        json=places_id
        # Query to
        # Get a list of places (DB model Place) around user's current location if lat/lng specified,
        # otherwise all places.

    #video=get_object_or_404(Musicas, video_id=video_id)
    return HttpResponse(json)
    #return render_to_response('comments/info_ajax_table.html', RequestContext(request, {'video':video}))

#
# checkins list
#
def checkins_list(request,places_id):
    json=places_id
    if request.method == 'GET':
        json+=request.GET.get('limit')
        json+=request.GET.get('offset')
    
        # Query to
        # Get a list of Check-ins for a specific Place.

    #video=get_object_or_404(Musicas, video_id=video_id)
    return HttpResponse(json)
    #return render_to_response('comments/info_ajax_table.html', RequestContext(request, {'video':video}))

#
# User
#
def user(request,user_id):
    
    if request.method == 'GET':
        json=user_id
    
        # Query to
        # Get a list of places (DB model Place) around user's current location if lat/lng specified,
        # otherwise all places.

    #video=get_object_or_404(Musicas, video_id=video_id)
    return HttpResponse(json)
    #return render_to_response('comments/info_ajax_table.html', RequestContext(request, {'video':video}))

#
# Users list
#
def users_list(request):
    json=''
    if request.method == 'GET':
        json+=request.GET.get('limit')
        json+=request.GET.get('offset')
    
        # Query to
        # Get a list of places (DB model Place) around user's current location if lat/lng specified,
        # otherwise all places.

    #video=get_object_or_404(Musicas, video_id=video_id)
    return HttpResponse(json)
    #return render_to_response('comments/info_ajax_table.html', RequestContext(request, {'video':video}))
