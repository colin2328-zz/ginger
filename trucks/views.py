from django.shortcuts import render
from django.http import HttpResponse
import logging
import operator


logger = logging.getLogger('trucks-console')


def home(request):
    # food_trucks = facebook_scaper.get_truck_counts(30)
    food_trucks = {"A" : 1,  "C": 5, "B" : 2, "D" : 4}
    sorted_trucks = sorted(food_trucks.iteritems(), key=operator.itemgetter(1))
    logger.debug(sorted_trucks)

    # print food_trucks

    return render(request, 'home.html', {'food_trucks' : sorted_trucks})