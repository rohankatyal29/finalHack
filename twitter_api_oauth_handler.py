import csv
import random

from twitter import * # https://github.com/sixohsix/twitter

def _get_api_auth_details():

        auth_details = list(csv.reader(open('api_keys.csv')))

	del(auth_details[0])

	random_auth_detail = random.choice(auth_details)

	api_key = {}

	api_key['consumer_key'] = random_auth_detail[0].strip()
	api_key['consumer_secret'] = random_auth_detail[1].strip()
	api_key['access_token'] = random_auth_detail[2].strip()
	api_key['access_token_secret'] = random_auth_detail[3].strip()

	return api_key



def get_api_client():
	auth_details = _get_api_auth_details()

	auth = OAuth(
		auth_details['access_token'],
		auth_details['access_token_secret'],
		auth_details['consumer_key'],
		auth_details['consumer_secret'])

	api = Twitter(auth = auth)

	return api

def get_auth_object():
	auth_details = _get_api_auth_details()

	auth = OAuth(
		auth_details['access_token'],
		auth_details['access_token_secret'],
		auth_details['consumer_key'],
		auth_details['consumer_secret'])

	return auth

if __name__ == '__main__':
	print get_auth_object()

	# api = get_api_client()
	# print api.trends_place(1)
