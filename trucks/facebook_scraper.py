#coding: utf8
import facebook
import re
import datetime, time
import hipchat
import urllib
import subprocess
import urlparse
import sys

event_name = "OffTheGridSF"

def get_fbook_token():    
	fbook_secret = '1f8984df22ec832578f690f8b370d97c'
	fbook_id = '432841790154607'

	oauth_args = dict(client_id     = fbook_id,
					  client_secret = fbook_secret,
					  grant_type    = 'client_credentials')
	oauth_curl_cmd = ['curl',
					  'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)]
	oauth_response = subprocess.Popen(oauth_curl_cmd,
									  stdout = subprocess.PIPE,
									  stderr = subprocess.PIPE).communicate()[0]
	try:
		fbook_token = urlparse.parse_qs(str(oauth_response))['access_token'][0]
		return fbook_token
	except KeyError:
		print('Unable to get access token')
		return None

def add_vendors_to_dict(vendors_list, diction):
	for vendor in vendors_list:
		if diction.has_key(vendor):
			diction[vendor] += 1
		else:
			diction[vendor] = 1

def calc_avg_word_count(lines):
	total_word_count = 0
	for line in lines[1:]:
		word_count = len(line.split(' '))
		total_word_count += word_count
	return float(total_word_count) /  float(len(lines) -1)

def get_vendors_list(text, id_no):
	date_time_regex = re.compile(ur'\d{1,2}th|1st|2nd|3rd|\d{1,2}:?\d{0,2}[AP]M|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday')

	text = text.replace('\r', '')
	text = text.replace(':', '')
	text = text.replace('\n \n', '\n\n')
	paragraphs = text.split("\n\n")	
	rtn_list = []	

	for paragraph in paragraphs:
		lines = paragraph.split("\n")
		lines = map(lambda line: line.strip(), lines) #get rid of extra spaces
		lines = filter(lambda line: line != '', lines) #get rid of empty lines
		if not lines:
			continue

		dates_found = 0
		for line in lines: #if there are multiple date strings in the paragraph, it is probably not a vendor list!
			results = date_time_regex.findall( line, re.I )
			length = len(results)
			if len(results):
				dates_found += length

		header = lines[0]
		if dates_found >= 2 or 'Location' in header or 'Time' in header or 'Music' in header or len(lines) < 2:
			# print header.encode('utf8')
			continue
		if 'Vendors' == header or 'Vendor' == header or 'Savory' == header or 'Sweet' == header or 'Alcohol' == header :
			rtn_list += lines[1:]
		elif calc_avg_word_count(lines) <= 5:
			if len(header.split(' ')) > 6:
				lines = lines[1:]
			rtn_list += lines

	return rtn_list	

def get_todays_vendors(address):
	try:
		today = str(datetime.date.today())
		graph = facebook.GraphAPI(get_fbook_token())
		off_grid_events = graph.get_connections(event_name, 'events')

		for event in off_grid_events['data']:
			if re.search(address, event['location'])  and re.search(today, event['start_time']):
				event = graph.get_object(event['id'], fields=['description', 'start_time', 'location'])
				break #found event with correct location and date!
		assert(re.search(address, event['location']) and re.search(today, event['start_time']))  #assert that location and time really does match
		return get_vendors_list(event['description'])
	except (facebook.GraphAPIError, Exception):
		return None


def post_todays_minna_vendors():
	address = '410 Minna St'
	hipchat_token = '35b7de36961929ed984c34bbfc0d08'
	hipchat_room_id = 320022
	hipchat_user = 'Food Fairy'
	hipster = hipchat.HipChat(token=hipchat_token)

	lst = get_todays_vendors(address)
	if lst: # make get_vendors_list returns something
		rtn_str = "Today's trucks: " + ', '.join(lst)
		print rtn_str
		# hipster.method('rooms/message', method='POST', parameters={'room_id': hipchat_room_id, 'from': hipchat_user, 'message': rtn_str})

def get_last_30_vendors():
	vendors_dict = {}
	try:
		graph = facebook.GraphAPI(get_fbook_token())
		until_ts = int(time.time()) #unix timestamp of today
		since_ts = until_ts - 60*60*24*30 #unix timestamp of 30 days ago
		off_grid_events = graph.get_connections(event_name, 'events', since=str(since_ts), until=str(until_ts))
		target_event_ids = []
		for event in off_grid_events['data']:
			target_event_ids.append( event['id'])
		events = graph.get_objects(cat='multiple', ids=target_event_ids, fields=['description', 'start_time', 'location'])
		
		for id_no in events:
			event = events[id_no]
			try:
				lst = get_vendors_list( event['description'], id_no)
			except Exception:
				pass
			if lst:
				rtn_str = id_no, "Today's trucks: " + ', '.join(lst)
				add_vendors_to_dict(lst, vendors_dict)
	except (facebook.GraphAPIError, Exception):
		pass
	finally:
		return vendors_dict


if __name__ == "__main__":
	print get_last_30_vendors()
	post_todays_minna_vendors()

