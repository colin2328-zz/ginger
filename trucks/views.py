from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    food_trucks = ['A', 'B', 'C', 'D']
    return render(request, 'home.html', {'food_trucks' : food_trucks})