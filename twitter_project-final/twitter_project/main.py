from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func
from sqlalchemy import create_engine, text
from datetime import datetime
import tweepy
import os
import configparser as cp
import uvicorn
from model import Tweet

app = FastAPI()
templates = Jinja2Templates(directory="templates")

config = cp.ConfigParser()
config.read("config.ini")

auth = tweepy.OAuthHandler(config["Default"]["consumer_key"], config["Default"]["consumer_secret"])
auth.set_access_token(config["Default"]["access_token"], config["Default"]["access_token_secret"])
api = tweepy.API(auth)

engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})
conn1 = engine.connect()



