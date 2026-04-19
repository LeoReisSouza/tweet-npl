"""Clientes da API do Twitter.

Uso:
    from src.api import create_client
    
    # Auto-detecta (GetXAPI primeiro, depois X API)
    client = create_client()
    
    # Ou especifica o provider
    client = create_client("getxapi")
    client = create_client("xapi")
    
    # Obtém tweets
    tweets = client.get_user_tweets("username", max_results=5)
    
    # Obtém info do usuário
    user = client.get_user("username")
"""

from ._base import TwitterClient
from .base import Tweet, User
from .factory import create_client, TwitterClientFactory

__all__ = [
    "TwitterClient",
    "Tweet", 
    "User",
    "create_client",
    "TwitterClientFactory",
]