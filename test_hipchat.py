import urllib2

url = "https://www.hipchat.com/gLly0MPv9?auth_token=35b7de36961929ed984c34bbfc0d08&room_id=320022&from=colin&message=hi"
request = urllib2.Request(url)
response = urllib2.urlopen(request)

print response.read()