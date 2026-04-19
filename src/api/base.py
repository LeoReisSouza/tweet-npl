from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Tweet:
    id: str
    text: str
    created_at: Optional[datetime]
    author_id: Optional[str] = None
    author_username: Optional[str] = None
    likes: int = 0
    retweets: int = 0
    replies: int = 0


@dataclass
class User:
    id: str
    username: str
    name: str
    followers_count: int = 0
    following_count: int = 0
    tweets_count: int = 0
    created_at: Optional[datetime] = None
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None