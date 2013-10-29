import facebook
import re
import datetime
import hipchat
import urllib
import subprocess
import urlparse


fbook_secret = '1f8984df22ec832578f690f8b370d97c'
fbook_id = '432841790154607'

# Trying to get an access token. Very awkward.
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
except KeyError:
    print('Unable to grab an access token!')
    exit()

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

address = '410 Minna St'
event_name = "OffTheGridSF"

next_wed = str(next_weekday(2)) 
next_fri = str(next_weekday(4))

graph = facebook.GraphAPI(fbook_token)
off_grid_events = graph.get_connections(event_name, 'events')
target_event_ids = []
for event in off_grid_events['data']:
    if re.search(address, event['location']) and (re.search(next_wed, event['start_time']) or re.search(next_fri, event['start_time'])) :
        target_event_ids.append( event['id'])


events = graph.get_objects(cat='multiple', ids=target_event_ids, fields=['description', 'start_time', 'location'])

hipchat_token = '35b7de36961929ed984c34bbfc0d08'
hipchat_room_id = 320022
hipchat_user = 'Food Fairy'
hipster = hipchat.HipChat(token=hipchat_token)

for id_no in events:
    rtn_str = ''
    event = events[id_no]
    #assert that location and time really does match
    assert(re.search(address, event['location']))
    if re.search(next_wed, event['start_time']):
        rtn_str += "Wednesday\'s trucks: "
    elif re.search(next_fri, event['start_time']):
        rtn_str += "Friday\'s trucks: "
    lst = process_vendors( event['description'])
    rtn_str += ', '.join(lst)
    hipster.method('rooms/message', method='POST', parameters={'room_id': hipchat_room_id, 'from': hipchat_user, 'message': rtn_str})






