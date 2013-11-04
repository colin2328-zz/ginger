#coding: utf8
import trucks.facebook_scraper as facebook_scraper
import hipchat


def post_todays_minna_vendors():
	"""
	Posts today's trucks on minna street to hipchat server
	"""
	address = '410 Minna St'
	hipchat_token = '35b7de36961929ed984c34bbfc0d08'
	hipchat_room_id = 320022
	hipchat_user = 'Food Fairy'
	hipster = hipchat.HipChat(token=hipchat_token)

	lst = facebook_scraper.get_todays_vendors(address)
	if lst: # make get_vendors_list is populated
		rtn_str = "Today's trucks: " + ', '.join(lst)
		print rtn_str
		# hipster.method('rooms/message', method='POST', parameters={'room_id': hipchat_room_id, 'from': hipchat_user, 'message': rtn_str})

if __name__ == "__main__":
	post_todays_minna_vendors()