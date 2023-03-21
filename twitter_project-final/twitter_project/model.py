from datetime import datetime
from pydantic import BaseModel


class Tweet(BaseModel):
    id: int
    username: str
    text: str
    updated_at: datetime
    created_at: datetime
    retweet_count: int
    favorite_count: int
    lang: str
