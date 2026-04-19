import requests
from datetime import datetime
from typing import Optional

from ._base import TwitterClient
from .base import Tweet, User


class GetXAPIClient(TwitterClient):
    """Cliente da API GetXAPI."""
    
    BASE_URL = "https://api.getxapi.com"
    
    def __init__(self, api_key: str):
        self._api_key = api_key
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    @property
    def provider(self) -> str:
        return "getxapi"
    
    def get_user_tweets(
        self, 
        username: str, 
        max_results: int = 5,
        exclude_retweets: bool = True
    ) -> list[Tweet]:
        """Obtém tweets de um usuário."""
        url = f"{self.BASE_URL}/twitter/user/tweets"
        
        params = {
            "userName": username,
            "count": min(max_results, 20)
        }
        
        response = self._session.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        tweets = []
        for item in data.get("tweets", []):
            text = item.get("text", "")
            
            # Filtra RTs pelo texto
            if exclude_retweets and text.startswith("RT @"):
                continue
            
            if not text:
                continue
            
            tweet = Tweet(
                id=item.get("id", ""),
                text=text,
                created_at=self._parse_datetime(item.get("createdAt")),
                author_id=item.get("author", {}).get("id"),
                author_username=item.get("author", {}).get("username"),
                likes=item.get("likeCount", 0),
                retweets=item.get("retweetCount", 0),
                replies=item.get("replyCount", 0)
            )
            tweets.append(tweet)
        
        return tweets
    
    def get_user(self, username: str) -> Optional[User]:
        """Obtém informações do perfil do usuário."""
        url = f"{self.BASE_URL}/twitter/user/info"
        
        params = {"userName": username}
        
        response = self._session.get(url, params=params)
        response.raise_for_status()
        
        data = response.json().get("data")
        
        if not data:
            return None
        
        return User(
            id=data.get("id", ""),
            username=data.get("username", ""),
            name=data.get("name", ""),
            followers_count=data.get("followers_count", 0),
            following_count=data.get("following_count", 0),
            tweets_count=data.get("tweets_count", 0),
            bio=data.get("description"),
            profile_image_url=data.get("profile_image_url")
        )
    
    def get_user_id(self, username: str) -> Optional[str]:
        """Obtém ID do usuário."""
        user = self.get_user(username)
        return user.id if user else None
    
    def _parse_datetime(self, dt_str: str) -> Optional[datetime]:
        if not dt_str:
            return None
        try:
            return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            pass
        try:
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(dt_str)
        except Exception:
            return None
    
    def test_connection(self) -> dict:
        """Testa se a API key é válida."""
        url = f"{self.BASE_URL}/twitter/account"
        response = self._session.get(url)
        return response.json() if response.status_code == 200 else {"error": "Conexão falhou"}