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
	# Assuming vendors text starts with vendors
	result = re.findall('Vendors:[\r\n\w+ \']*\r\n\r\n', text)
	print result
	if result:
		split = result[0].split('\r\n')
		return split[1:-3]

token = 'CAACEdEose0cBAHrRy2storpmKC56lKnAafEtGxvdS4HZArZAzOTHUrtZBqfC5ZBMp9KEpTYzBqT6pVfnR6upK6OgfdjP3ZCj5TQP6dL2v5igwQQ7O4kuZCfyyv4NBHLjIXPuM78XV0ZBAZCxW6kHbCmi9IFbbH7ig2EiOiRRUunZBIXTZCzp0bqQcVfgA9CNb7WYQRBZA4reSxMgAZDZD'
address = '410 Minna St'
event_name = "OffTheGridSF"


# text = """Every Wednesday and Friday, this market is perfect for lunch! Nestled in the Minna St. tunnel (at 5th St.), this location is great for escaping the fog or rain. Check out live music every Friday.\r\n\r\nLocation: 5th St. @ Minna St.\r\nTime: 11:00am-2:00pm\r\n\r\n \ 
# Vendors:\r\nFins on the Hoof\r\nPhat Thai\r\nTandoori Chicken USA\r\nVoodoo Van\r\nTres Truck\r\n\r\n\r\nCATERING NEEDS? Have OtG cater your next event! Get started by visiting offthegridsf.com/catering."""


next_wed = str(next_weekday(2)) 
next_fri = str(next_weekday(4))

graph = facebook.GraphAPI(token)
off_grid_events = graph.get_connections(event_name, 'events')
target_event_ids = []
for event in off_grid_events['data']:
	if re.search(address, event['location']) and (re.search(next_wed, event['start_time']) or re.search(next_fri, event['start_time'])) :
		target_event_ids.append( event['id'])


events = graph.get_objects(cat='multiple', ids=target_event_ids, fields=['description'])
#todo: assert event location is on Minna
for id_no in events:
	print id_no
	event = events[id_no]
	lst = process_vendors( event['description'])
	print lst

# profile = graph.get_object("me")
# friends = graph.get_connections("me", "friends")

# friend_list = [friend['name'] for friend in friends['data']]

# print friend_list


