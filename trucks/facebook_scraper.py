import facebook
import re
import datetime
import hipchat
import urllib
import subprocess
import urlparse

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

def get_vendors_list(text):
    # Assuming vendor's list text starts and ends with the following strings
    text = text.replace('\r', '')
    start_string = r'Vendors:'
    end_string = r'\n\n'
    regex_string = start_string + r"[\n\w ']*" + end_string
    result = re.findall( regex_string , text)
    if result:
        split = result[0].split('\n')
        return split[1:-3] #remove start string and end strings

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
    except (facebook.GraphAPIError, IndexError):
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
    graph = facebook.GraphAPI(get_fbook_token())
    off_grid_events = graph.get_connections(event_name, 'events')
    target_event_ids = []
    for event in off_grid_events['data']:
        if re.search(address, event['location'])  and re.search(today, event['start_time']):
            target_event_ids.append( event['id'])
    events = graph.get_objects(cat='multiple', ids=target_event_ids, fields=['description', 'start_time', 'location'])    

    for id_no in events:
        event = events[id_no]
        assert(re.search(address, event['location']) and re.search(today, event['start_time']))  #assert that location and time really does match
        lst = get_vendors_list( event['description'])
        if lst:
            rtn_str = "Today's trucks: " + ', '.join(lst)
            print rtn_str
            # hipster.method('rooms/message', method='POST', parameters={'room_id': hipchat_room_id, 'from': hipchat_user, 'message': rtn_str})


if __name__ == "__main__":
    post_todays_minna_vendors()

