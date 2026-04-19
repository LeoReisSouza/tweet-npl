import os
from typing import Optional

from dotenv import load_dotenv

from ._base import TwitterClient
from .getxapi_client import GetXAPIClient
from .twitter_client import XTwitterClient


load_dotenv()


class TwitterClientFactory:
    """Factory para criar clientes da API do Twitter."""
    
    PROVIDERS = {
        "getxapi": GetXAPIClient,
        "xapi": XTwitterClient,
    }
    
    @classmethod
    def create(
        cls, 
        provider: Optional[str] = None,
        api_key: Optional[str] = None,
        bearer_token: Optional[str] = None
    ) -> TwitterClient:
        """Cria um cliente da API do Twitter."""
        if api_key is None:
            api_key = os.getenv("GETXAPI_KEY")
        if bearer_token is None:
            bearer_token = os.getenv("X_BEARER_TOKEN")
        
        if provider is None or provider == "auto":
            provider = cls._detect_provider(api_key, bearer_token)
        
        if provider not in cls.PROVIDERS:
            raise ValueError(f"Provider desconhecido: {provider}")
        
        if provider == "getxapi":
            if not api_key:
                raise ValueError("GETXAPI_KEY é necessário para o provider getxapi")
            return GetXAPIClient(api_key)
        else:
            if not bearer_token:
                raise ValueError("X_BEARER_TOKEN é necessário para o provider xapi")
            return XTwitterClient(bearer_token)
    
    @classmethod
    def _detect_provider(cls, api_key: Optional[str], bearer_token: Optional[str]) -> str:
        """Detecta automaticamente qual provider usar (prioridade: getxapi -> xapi)."""
        if api_key:
            return "getxapi"
        if bearer_token:
            return "xapi"
        raise ValueError("Nenhuma credencial encontrada. Configure GETXAPI_KEY ou X_BEARER_TOKEN")


def create_client(
    provider: Optional[str] = None,
    api_key: Optional[str] = None,
    bearer_token: Optional[str] = None
) -> TwitterClient:
    """Função para criar um cliente da API.
    
    Uso:
        client = create_client()            # auto-detecta
        client = create_client("getxapi")
        client = create_client("xapi", bearer_token="...")
    """
    return TwitterClientFactory.create(provider, api_key, bearer_token)