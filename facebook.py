import requests # pip install requests
import json
from pymongo import MongoClient

db_name = 'project-1'
collection_name = 'facebook'

def fb_data(key):
    db_client = MongoClient('localhost', 27017)
    db = db_client[db_name]
    keyword=key
    base_url = 'https://graph.facebook.com/'+keyword

    # Get 10 likes for 10 friends
    fields = 'id,name,posts'

    url = '%s?fields=%s&access_token=%s' % \
        (base_url, fields, 'CAACEdEose0cBAHkVwKki4eUVsDe1DrTbZCZBz7JhDSgn4glqmtmyV1lMO3auvSIwO8OGXwpgmcSOZBNrka8idSVE8VZCHZCzdZAKixZAM7NXOdRDi0XgRq8TKLdtFFmWN006A0Qb8tcYruWXkG20m9ZCpzN5HZCUv38M1XKIhDyOhZC87W012vIEQKCZBNMjJjEJzwWdBm4O2PZBNAZDZD')


    print url
    content = requests.get(url).json()

    # Pretty-print the JSON and display it
    ##posts = json.dumps(content, indent=1)
    ##print content

    db[collection_name].insert(content)

##fb_data('CERCatIIITD')
