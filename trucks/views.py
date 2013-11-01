from django.shortcuts import render
from django.http import HttpResponse
import logging
import operator
import facebook_scraper


logger = logging.getLogger('trucks-console')


def home(request):
    food_trucks = facebook_scraper.get_last_30_vendors()
    # food_trucks = {"A" : 1,  "C": 5, "B" : 2, "D" : 4}
    sorted_trucks = sorted(food_trucks.iteritems(), key=operator.itemgetter(1), reverse=True)
    logger.debug(sorted_trucks)

    # print food_trucks

    return render(request, 'home.html', {'food_trucks' : sorted_trucks})