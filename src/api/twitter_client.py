import tweepy
from datetime import datetime
from typing import Optional

from ._base import TwitterClient
from .base import Tweet, User


class XTwitterClient(TwitterClient):
    """Cliente da API oficial do X (Twitter)."""
    
    def __init__(self, bearer_token: str):
        self._client = tweepy.Client(bearer_token=bearer_token)
    
    @property
    def provider(self) -> str:
        return "xapi"
    
    def get_user_tweets(
        self, 
        username: str, 
        max_results: int = 5,
        exclude_retweets: bool = True
    ) -> list[Tweet]:
        """Obtém tweets de um usuário."""
        user_id = self.get_user_id(username)
        if not user_id:
            return []
        
        exclude = 'retweets' if exclude_retweets else None
        
        response = self._client.get_users_tweets(
            id=user_id,
            max_results=max_results,
            exclude=exclude,
            tweet_fields=['created_at', 'public_metrics', 'author_id']
        )
        
        if not response.data:
            return []
        
        tweets = []
        for item in response.data:
            metrics = item.public_metrics or {}
            tweet = Tweet(
                id=item.id,
                text=item.text,
                created_at=item.created_at,
                likes=metrics.get('like_count', 0),
                retweets=metrics.get('retweet_count', 0),
                replies=metrics.get('reply_count', 0)
            )
            tweets.append(tweet)
        
        return tweets
    
    def get_user(self, username: str) -> Optional[User]:
        """Obtém informações do perfil do usuário."""
        response = self._client.get_user(username=username)
        
        if not response.data:
            return None
        
        data = response.data
        return User(
            id=data.id,
            username=data.username,
            name=data.name,
            followers_count=getattr(data, 'public_metrics', {}).get('followers_count', 0),
            following_count=getattr(data, 'public_metrics', {}).get('following_count', 0),
            tweets_count=getattr(data, 'public_metrics', {}).get('tweet_count', 0),
            bio=getattr(data, 'description', None)
        )
    
    def get_user_id(self, username: str) -> Optional[str]:
        """Obtém ID do usuário."""
        response = self._client.get_user(username=username)
        
        if not response.data:
            return None
        
        return response.data.id
    
    def search(
        self, 
        query: str, 
        max_results: int = 20,
        product: str = "Latest"
    ) -> list[Tweet]:
        """Pesquisa tweets usando Advanced Search."""
        # Ignora 'product' - X API não suporta
        response = self._client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=['created_at', 'public_metrics', 'author_id']
        )
        
        if not response.data:
            return []
        
        tweets = []
        for item in response.data:
            metrics = item.public_metrics or {}
            tweet = Tweet(
                id=item.id,
                text=item.text,
                created_at=item.created_at,
                likes=metrics.get('like_count', 0),
                retweets=metrics.get('retweet_count', 0),
                replies=metrics.get('reply_count', 0)
            )
            tweets.append(tweet)
        
        return tweets
    
    def test_connection(self) -> dict:
        """Testa se as credenciais são válidas."""
        try:
            response = self._client.get_me()
            return {
                "status": "conectado",
                "user": response.data.username if response.data else None
            }
        except Exception as e:
            return {"status": "erro", "message": str(e)}