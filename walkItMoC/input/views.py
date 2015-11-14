from django.shortcuts import render
from django.http import Http404

# Create your views here.

def home(request):
	context = {'message': 'Your location:'}
	return render( request, 'input/index.html', context)
