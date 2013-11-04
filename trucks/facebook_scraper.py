#coding: utf8
import facebook
import re
import datetime
import dateutil.parser as dateparser
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


def calc_avg_word_count(lines):
	total_word_count = 0
	for line in lines[1:]:
		word_count = len(line.split(' '))
		total_word_count += word_count
	return float(total_word_count) /  float(len(lines) -1)

def scrape_vendors_list(text):
	"""
	argument: text - a string containing the information from a vendor's page
	return: a list of vendors in the text, or empty list

	Uses a hardcoded decision tree to identify vendors. If I had more time, I would use a more sophisticated method (such as defining several metrics/heuristics
	and using ML to classify a line as a vendor or not)
	"""
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

def get_events(since, until):
	"""
	arguments: since and until are unix timestamps or datetime.date objects
	return: list of event objects or empty list

	"""
	try:
		graph = facebook.GraphAPI(get_fbook_token())
		off_grid_events = graph.get_connections(event_name, 'events', since=str(since), until=str(until))

		target_event_ids = []
		for event in off_grid_events['data']:
			target_event_ids.append( event['id'])
		return graph.get_objects(cat='multiple', ids=target_event_ids, fields=['description', 'start_time', 'location'])
	except (facebook.GraphAPIError, Exception) as e:
		print 'exception', e
		return []

def scrape_todays_vendors(address):
	"""
	arguments: address - string
	return: list of vendor names or empty list
	"""
	today = datetime.date.today()
	tomorrow = today + datetime.timedelta(1)
	events = get_events(today, tomorrow)
	
	for id_no in events:
		event = events[id_no]
		if re.search(address, event['location'])  and re.search(str(today), event['start_time']): #found event with correct location and date!

			return scrape_vendors_list(event['description'])
	return []

def scrape_last_30_days_vendors():
	"""
	return: a list of (id (int), date (datetime.date), and vendors_list) tuples  or empty list
	"""
	today = datetime.date.today()
	last_month = today - datetime.timedelta(30)
	events = get_events(last_month, today)
	
	rtn_lst = []
	for id_no in events:
		event = events[id_no]
		lst = scrape_vendors_list( event['description'])
		if lst:
			date = dateparser.parse(event['start_time']).date()
			rtn_lst.append((id_no, date, lst))
	return rtn_lst


if __name__ == "__main__":
	print scrape_last_30_days_vendors()

