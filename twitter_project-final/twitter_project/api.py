from main import app, api, templates, conn1
from fastapi import Request, Response, status, HTTPException
from sqlalchemy import create_engine, text
from model import Tweet
from datetime import datetime
import uvicorn


@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/tweets")
def get_tweets(request: Request, response: Response, username: str):
    try:
        tweets = api.user_timeline(screen_name=username, count=100)
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")

    rows = conn1.execute(text(f"SELECT * FROM tweet WHERE username in ('{username}') ")).fetchall()
    for tweet in rows:
        if username == tweet[1]:
            break
    else:
        for tweet in tweets:
            tweet_obj = Tweet(username=username, id=tweet.id, text=tweet.text, updated_at=datetime.now(), created_at=tweet.created_at, retweet_count=tweet.retweet_count, favorite_count=tweet.favorite_count, lang=tweet.lang)
            conn1.execute(
                text(
                    """
                INSERT INTO tweet (username, id, updated_at , created_at, retweet_count, favorite_count, text, lang)
                VALUES (:username, :id, :updated_at, :created_at, :retweet_count, :favorite_count, :text, :lang)
            """
                ),
                tweet_obj.dict(),
            )

            rows = conn1.execute(text(f"SELECT * FROM tweet WHERE username in ('{username}') ")).fetchall()

    print(f"SELECT * FROM tweet WHERE username in ('{username}') ")
    if not rows:
        raise HTTPException(status_code=404, detail='No tweets found for screen_name "{}"'.format(username))

    return templates.TemplateResponse("tweets.html", {"request": request, "tweets": rows})


@app.get("/search")
def search_tweets(request: Request, searchbox: str):
    rows = conn1.execute(text(f"SELECT * FROM tweet WHERE text LIKE '%{searchbox}%'")).fetchall()
    print("rows", rows)
    if not rows:
        raise HTTPException(status_code=404, detail='No tweets found for search term "{}"'.format(searchbox))

    return templates.TemplateResponse("tweets.html", {"request": request, "tweets": rows})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3007, reload=True)
