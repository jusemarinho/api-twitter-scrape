import tweepy
from dotenv import load_dotenv
import os
from collections import namedtuple


class Scrape:

    def __init__(self):
        load_dotenv()

    def initialize(self):
        bearer_token = os.getenv('BEARER_TOKEN')
        self.client = tweepy.Client(bearer_token = bearer_token)
        return self

    def get_tweets(self, words, max_results):
        # public_tweets = self.api.search_all_tweets(query = words, max_results = max_results)
        # users = self.client.get_users(usernames=["iamjusee", "kalilgm"])
        # for user in users:
        #     print(user)
        pass

    def get_id_user_by_usernames(self, users):
        users = self.client.get_users(usernames = users)
        return [{'id': user.id, 'name': user.name} for user in users.data]

    def get_tweets_from_words(self, word):
        query = f'{word} lang:pt -is:retweet'
        tweets = self.client.search_recent_tweets(
                query=query,
                tweet_fields=['context_annotations', 'created_at', 'public_metrics', 'source', 'geo'],
                max_results=100,  
                place_fields = ['place_type', 'geo'],
                expansions=['author_id', 'geo.place_id']
            )
        users = {user["id"]: user for user in tweets.includes['users']}
        Tweet = namedtuple("Tweet", ["name", "tweet", "likes", "retweets", "criado_em", "source"])
        tweets_tuple = []
        for tweet in tweets.data:
            if users[tweet.author_id]:
                user = users[tweet.author_id]
                tweets_tuple.append(Tweet(user.name, 
                                        tweet.text, 
                                        tweet.public_metrics['like_count'], 
                                        tweet.public_metrics['retweet_count'], 
                                        tweet.created_at.strftime('%d-%m-%Y %H:%M:%S'), 
                                        tweet.source
                                        )
                                    )

        return tweets_tuple

    # def get_user_by_id