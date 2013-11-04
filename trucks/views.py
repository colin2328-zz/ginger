from django.shortcuts import render
from django.http import HttpResponse
import logging
import operator
import event_persistance
from django.conf import settings


logger = logging.getLogger('trucks-console')


def home(request):
	food_trucks = event_persistance.retrieve_last_30_days_vendors()
	sorted_trucks = sorted(food_trucks.iteritems(), key=operator.itemgetter(1), reverse=True)
	return render(request, 'home.html', {'food_trucks' : sorted_trucks})

def about(request):
	return render(request, 'about.html', {})