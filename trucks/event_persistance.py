#coding: utf8
import trucks.facebook_scraper as facebook_scraper
from trucks.models import Truck, Event
import datetime

def add_vendors_to_dict(vendors_list, diction):
	"""
	Helper function to add to counting dict
	"""
	for vendor in vendors_list:
		if diction.has_key(vendor.name):
			diction[vendor.name] += 1
		else:
			diction[vendor.name] = 1


def store_last_30_days_vendors():
	"""
	stores results from scraping in database from last 30 days

	If had more time, might want to consider entity resolution! (in case a vendor was mispelled etc.)
	"""
	event_list = facebook_scraper.scrape_last_30_days_vendors()

	for event in event_list:
		(id_no, date, truck_name_list) = event
		id_no = str(id_no)
		try:
			event = Event.objects.get(id=id_no)
		except Event.DoesNotExist: #only store event if it is not already in the database!
			event = Event(id=id_no, date=date)
			event.save()
			for truck_name in truck_name_list:
				try:
					truck = Truck.objects.get(name=truck_name)
				except Truck.DoesNotExist:
					truck = Truck(name=truck_name)
					truck.save()
				event.trucks.add(truck)
			event.save()


def retrieve_last_30_days_vendors():
	"""
	Retrieve vendors list from database for last 30 days
	Return: dictionary of vendor names to counts to present to controller
	"""
	vendors_dict = {}
	today = datetime.date.today()
	last_month = today - datetime.timedelta(30)
	events = Event.objects.filter(date__range=(last_month, today))
	for event in events:
		add_vendors_to_dict(event.trucks.all(), vendors_dict)
	return vendors_dict