import facebook
import re
import datetime

def next_weekday(weekday_int):
	# weekday_int: 0 = Monday, 1=Tuesday, 2=Wednesday...
	today = datetime.date.today()
	days_ahead = weekday_int - today.weekday()
	if days_ahead < 0: # Target day already happened this week
		days_ahead += 7
	return today + datetime.timedelta(days_ahead)

def process_vendors(text):
	# Assuming text starts and ends with the following strings
	start_string = 'Vendors:'
	end_string = '\r\n\r\n'
	result = re.findall( start_string + '[\r\n\w+ \']*' + end_string, text)
	if result:
		split = result[0].split('\r\n')
		return split[1:-3] #remove start string and end strings

token = 'CAACEdEose0cBAHrRy2storpmKC56lKnAafEtGxvdS4HZArZAzOTHUrtZBqfC5ZBMp9KEpTYzBqT6pVfnR6upK6OgfdjP3ZCj5TQP6dL2v5igwQQ7O4kuZCfyyv4NBHLjIXPuM78XV0ZBAZCxW6kHbCmi9IFbbH7ig2EiOiRRUunZBIXTZCzp0bqQcVfgA9CNb7WYQRBZA4reSxMgAZDZD'
address = '410 Minna St'
event_name = "OffTheGridSF"

next_wed = str(next_weekday(2)) 
next_fri = str(next_weekday(4))

graph = facebook.GraphAPI(token)
off_grid_events = graph.get_connections(event_name, 'events')
target_event_ids = []
for event in off_grid_events['data']:
	if re.search(address, event['location']) and (re.search(next_wed, event['start_time']) or re.search(next_fri, event['start_time'])) :
		target_event_ids.append( event['id'])


events = graph.get_objects(cat='multiple', ids=target_event_ids, fields=['description', 'start_time', 'location'])
for id_no in events:
	event = events[id_no]
	#assert that location and time really does match
	assert(re.search(address, event['location']))
	if re.search(next_wed, event['start_time']):
		print 'Wednesday truck'
	elif re.search(next_fri, event['start_time']):
		print 'Friday truck'
	lst = process_vendors( event['description'])
	print lst


