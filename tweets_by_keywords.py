import time
import twitter_api_oauth_handler as tw
import json

from pymongo import MongoClient

db_name = 'project-1'
collection_name = 'keyword'

def get_tweets_by_keyword(
    api,
    keyword,
    max_id,
    count = 100,
    
    exclude_replies = False,
    include_rts = True):
    tweets = []
    if max_id != None:
        
        tweets = api.search.tweets(q=keyword,
                                   max_id = max_id,
                                   count = count,
                                   exclude_replies = exclude_replies,
                                   include_rts = include_rts)

        
    else:
        
        tweets = api.search.tweets(q=keyword,
                                   max_id = max_id,
                                   count = count,
                                   exclude_replies = exclude_replies,
                                   include_rts = include_rts)

    return tweets

def main(keyword):
        
    db_client = MongoClient('localhost', 27017)
    db = db_client[db_name]
    keywords = keyword
    max_id = None

    while True:
        api = tw.get_api_client()
        tweets = get_tweets_by_keyword(api, keywords, max_id)
        
        if len(tweets) > 0:
            try:
            # Parse the data returned to get max_id to be passed in consequent call.
                next_results_url_params    = tweets['search_metadata']['next_results']
                max_id        = next_results_url_params.split('max_id=')[1].split('&')[0]
            except:
            # No more next pages
                break
            
            for status in tweets['statuses']:
                if 'media' in status['entities']:
                      
    ##                media = status['entities']['media'][0]['media_url']
                    db[collection_name+'_'+keyword].insert(status)
##                    print status
##                    print 'Inserted', status['id']

