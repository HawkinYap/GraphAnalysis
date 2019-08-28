from django.shortcuts import render
from django.http import HttpResponse
import json
import time

from backend import models

# Create your views here.
def saveRect(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		print(params)
		try:
			models.Rectangle.objects.create(time=params['time'], name=params['name'], x1=params['x1'], y1=params['y1'], x2=params['x2'], y2=params['y2'])
			return HttpResponse(json.dumps({'state': 'success'}), content_type='application/json')
		except:
			return HttpResponse(json.dumps({'state': 'fail'}), content_type='application/json')

def saveDuration(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		print(params)
		try:
			# now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) 
			models.Duration.objects.create(time=params['time'], name=params['name'], consumingtime=params['consumingtime'])
			return HttpResponse(json.dumps({'state': 'success'}), content_type='application/json')
		except:
			return HttpResponse(json.dumps({'state': 'fail'}), content_type='application/json')

def readRect(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		print(params)
		filter_data = models.Rectangle.objects.filter(name=params['name']).values()
		return HttpResponse(json.dumps({'datum': list(filter_data)}), content_type='application/json')