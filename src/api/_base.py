from abc import ABC, abstractmethod
from typing import Optional

from .base import Tweet, User


class TwitterClient(ABC):
    """Classe base abstrata para clientes da API do Twitter."""
    
    @abstractmethod
    def get_user_tweets(
        self, 
        username: str, 
        max_results: int = 5,
        exclude_retweets: bool = True
    ) -> list[Tweet]:
        """Obtém tweets do perfil de um usuário."""
        pass
    
    @abstractmethod
    def get_user(self, username: str) -> Optional[User]:
        """Obtém informações do perfil do usuário."""
        pass
    
    @abstractmethod
    def get_user_id(self, username: str) -> Optional[str]:
        """Obtém o ID do usuário a partir do username."""
        pass
    
    @property
    @abstractmethod
    def provider(self) -> str:
        """Retorna o nome do provider (xapi | getxapi)."""
        pass