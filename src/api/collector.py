import tweepy
import os
import json
from datetime import datetime


class TwitterCollector:
    def __init__(self, bearer_token: str):
        self.client = tweepy.Client(bearer_token=bearer_token)
    
    def get_user_id(self, username: str) -> str | None:
        user = self.client.get_user(username=username)
        if user.data:
            return user.data.id
        return None
    
    def get_user_tweets(self, username: str, max_results: int = 5, exclude_retweets: bool = True):
        user_id = self.get_user_id(username)
        if not user_id:
            print(f"Usuário {username} não encontrado")
            return []
        
        exclude = 'retweets' if exclude_retweets else None
        
        tweets = self.client.get_users_tweets(
            id=user_id,
            max_results=max_results,
            exclude=exclude,
            tweet_fields=['created_at', 'text', 'public_metrics']
        )
        return tweets.data if tweets.data else []
    
    def search_tweets(self, query: str, max_results: int = 100):
        tweets = self.client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=['created_at', 'author_id', 'text', 'public_metrics']
        )
        return tweets.data
    
    def save_tweets(self, tweets, filepath: str):
        data = []
        for tweet in tweets:
            data.append({
                'id': tweet.id,
                'text': tweet.text,
                'created_at': tweet.created_at,
                'likes': tweet.public_metrics.get('like_count', 0),
                'retweets': tweet.public_metrics.get('retweet_count', 0),
            })
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"Salvos {len(data)} tweets em {filepath}")
        return data