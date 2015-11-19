import time
import twitter_api_oauth_handler as tw
from pymongo import MongoClient

db_name = 'psosm_end_sem'
collection_name = 'users'

def get_tweets_by_user(
        api,
        screen_name,
        max_id ,
        count = 200,
        exclude_replies = False,
        include_rts = True):
        tweets = []

        if max_id != None:
                tweets = api.statuses.user_timeline(
                        screen_name = screen_name,
                        max_id = max_id,
                        count = count,
                        exclude_replies = exclude_replies,
                        include_rts = include_rts)

                del(tweets[0])
        else:
                tweets = api.statuses.user_timeline(
                        screen_name = screen_name,
                        count = count,
                        exclude_replies = exclude_replies,
                        include_rts = include_rts)

        return tweets

def main(users):

        db_client = MongoClient('localhost', 27017)
        db = db_client[db_name]
        users=users
        
        for user in users:
                max_id = None
                while True:
                        api = tw.get_api_client()
                        tweets = get_tweets_by_user(api, user, max_id)
                        if len(tweets) > 0:
                                max_id = tweets[-1]['id']
                                for tweet in tweets:
                                        db[collection_name+'_'+user].insert(tweet)
        ##                              db['tweets_'+str(tweet['user']['screen_name'])].insert(tweet)
                                        print 'Inserted', tweet['id']
                        else:
                                break

##users = ['CPBlr']
##main(users)
