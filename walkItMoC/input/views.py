from django.shortcuts import render
from django.http import Http404

import urllib2
import json

from datetime import datetime
import dateutil.parser

tflAPI='https://api.tfl.gov.uk/'
tflAuth='?app_id=d7cf5261&app_key=97f8c33e2afb97aed1cc3b17c93a023e'

temp = '[{"$type": "Tfl.Api.Presentation.Entities.Prediction, Tfl.Api.Presentation.Entities",\
    "id": "402709115",\
    "operationType": 1,\
    "vehicleId": "YY15CNN",\
    "naptanId": "490000050E",\
    "stationName": "Clapham Common Station",\
    "lineId": "322",\
    "lineName": "322",\
    "platformName": "E",\
    "direction": "inbound",\
    "destinationNaptanId": "",\
    "destinationName": "Crystal Palace",\
    "timestamp": "2015-11-14T22:59:04.883Z",\
    "timeToStation": 705,\
    "currentLocation": "",\
    "towards": "Brixton or Clapham North",\
    "expectedArrival": "2015-11-14T23:10:50Z",\
    "timeToLive": "2015-11-14T23:11:20Z",\
    "modeName": "bus"\
  },\
  {\
    "$type": "Tfl.Api.Presentation.Entities.Prediction, Tfl.Api.Presentation.Entities",\
    "id": "-1800506313",\
    "operationType": 1,\
    "vehicleId": "LX09FAF",\
    "naptanId": "490000050E",\
    "stationName": "Clapham Common Station",\
    "lineId": "345",\
    "lineName": "345",\
    "platformName": "E",\
    "direction": "inbound",\
    "destinationNaptanId": "",\
    "destinationName": "Peckham",\
    "timestamp": "2015-11-14T22:59:33.824Z",\
    "timeToStation": 442,\
    "currentLocation": "",\
    "towards": "Brixton or Clapham North",\
    "expectedArrival": "2015-11-14T23:06:56Z",\
    "timeToLive": "2015-11-14T23:07:26Z",\
    "modeName": "bus"\
  },\
  {\
    "$type": "Tfl.Api.Presentation.Entities.Prediction, Tfl.Api.Presentation.Entities",\
    "id": "-1848893058",\
    "operationType": 1,\
    "vehicleId": "SN61BHD",\
    "naptanId": "490000050E",\
    "stationName": "Clapham Common Station",\
    "lineId": "345",\
    "lineName": "345",\
    "platformName": "E",\
    "direction": "inbound",\
    "destinationNaptanId": "",\
    "destinationName": "Peckham",\
    "timestamp": "2015-11-14T22:59:45.119Z",\
    "timeToStation": 900,\
    "currentLocation": "",\
    "towards": "Brixton or Clapham North",\
    "expectedArrival": "2015-11-14T23:14:46Z",\
    "timeToLive": "2015-11-14T23:15:16Z",\
    "modeName": "bus"\
  },\
  {\
    "$type": "Tfl.Api.Presentation.Entities.Prediction, Tfl.Api.Presentation.Entities",\
    "id": "-2009948351",\
    "operationType": 1,\
    "vehicleId": "SN61BKG",\
    "naptanId": "490000050E",\
    "stationName": "Clapham Common Station",\
    "lineId": "345",\
    "lineName": "345",\
    "platformName": "E",\
    "direction": "inbound",\
    "destinationNaptanId": "",\
    "destinationName": "Peckham",\
    "timestamp": "2015-11-14T22:59:33.824Z",\
    "timeToStation": 1465,\
    "currentLocation": "",\
    "towards": "Brixton or Clapham North",\
    "expectedArrival": "2015-11-14T23:23:59Z",\
    "timeToLive": "2015-11-14T23:24:29Z",\
    "modeName": "bus"\
  }]'
  
from django.core.urlresolvers import reverse
# Create your views here.

def home(request):
	context = {'message': 'Your location:'}
	return render( request, 'input/index.html', context)

def stop(request):

	stopId='490000050E'
	res = urllib2.urlopen('{}{}{}{}'.format(tflAPI,'StopPoint/',stopId,'/Arrivals'))
	data = json.load(res)

	print 'data length: {}'.format(len(data))
	arrivals=[]
	time_now=datetime.now()
	print 'time now: {}'.format(time_now)
	for i, arrival in enumerate(data):
		arrivals.append( {'lineName' : arrival['lineName']} )
		#print 'arrivals dict: {}'.format(arrivals)
		expected = dateutil.parser.parse(arrival['expectedArrival'])
		expected = expected.replace(tzinfo=None)
		#print 'expected: {}'.format(expected)
		#print 'expected clean: {}'.format(str(expected-time_now)[2:4])
		if expected<time_now:#-datetime.timedelta(minutes=1):
			arrivals[i]['expectedArrival']='is due'
		else:
			arrivals[i]['expectedArrival']='in {} min.'.format(str(expected-time_now)[2:4])
	
	print arrivals

	if data:
		current_stop=data[0]['stationName']
	else:
		current_stop='No buses coming :-('
	context = {
		'message': '{}'.format(current_stop),
		'arrivals': arrivals,
		}
	return render( request, 'input/stop.html', context)

def paper(request):
	print reverse('stop')
	context = {
		'links': reverse('stop'),
		'paper_choice': 'Ticket',
		'paper_price': '9.50',
		'message': 'Get a ticket {}'.format('here'),
		}
	return render (request, 'input/getpaper.html', context)

def coffee(request):
	print reverse('stop')
	context = {
		'links': reverse('stop'),
		'coffee_choice': 'Juice',
		'coffee_price': '2.40',
		'coffee_price_data': '250',
		'message': 'Get a tomato juice at {}'.format('Squiezer'),
		}
	return render (request, 'input/getcoffee.html', context)

def walk(request):
	#stopId='490000050E'
	#res = urllib2.urlopen('{}{}{}{}'.format(tflAPI,'StopPoint/',stopId,'/Arrivals'))
	#data = json.load(res)
	
	line='345'
	res = urllib2.urlopen('{}{}{}{}'.format(tflAPI,'Line/',line,'/StopPoints'))
	data = json.load(res)
	origin=(data[0]['lat'] ,data[0]['lon'])
	
	vicinity=[]
	for stop in data:
		if abs(stop['lat']-origin[0]) < 0.002 and abs(stop['lon']-origin[1]) > 0.002:
			vicinity.append( (stop['commonName']) )#, stop['lat'], stop['lon']) )
	print 'len vicinity: {}'.format( len(vicinity) )
	context = {'close_stations': vicinity[0]}
	return render (request, 'input/gowalk.html', context)

#"https://api.tfl.gov.uk/StopPoint/?lat=51.461411&lon=-0.138759&stopTypes=NaptanPublicBusCoachTram&radius=100&app_id=d7cf5261&app_key=97f8c33e2afb97aed1cc3b17c93a023e"

def about(request):
	context = {}
	return render (request, 'input/about.html', context)