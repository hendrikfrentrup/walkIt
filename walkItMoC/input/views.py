from django.shortcuts import render
from django.http import Http404

import urllib2
import json

from datetime import datetime
import dateutil.parser

tflAPI='https://api.tfl.gov.uk/'
tflAuth='?app_id=d7cf5261&app_key=97f8c33e2afb97aed1cc3b17c93a023e'

temp=[]

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
		if expected<time_now:
			arrivals[i]['expectedArrival']='is due'
		else:
			arrivals[i]['expectedArrival']='in {} min.'.format(str(expected-time_now)[2:4])
	
	print arrivals
	context = {
		'message': 'Your Stop: {}'.format(data[1]['stationName']),
		'arrivals': arrivals,
		}
	return render( request, 'input/stop.html', context)


