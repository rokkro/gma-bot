import tweepy
from src.config import config
from os.path import dirname,abspath
from src.text_parse import form_phrase
import random

auth = tweepy.OAuthHandler(config['TWITTER']['ckey'], config['TWITTER']['csecret'])
auth.set_access_token(config['TWITTER']['atoken'],config['TWITTER']['asecret'])

#Initialize tweepy api with authentication keys
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

def get_lines(filename):
    items = []
    with open(dirname(dirname(abspath(__file__))) + "/" + filename) as file:
        for line in file:
            if line.startswith("///"):
                continue
            items.append(line.replace("\n",""))
    return items

def text_get(text_content):
    intro = get_lines("intro.txt")
    ending = get_lines("end.txt")
    text = text_content
    result = form_phrase(intro, text, ending, check_words=True, capitalized=random.choice([True,False]), extras=random.choice([True,False]))
    print(result)

text_get("i like pie")
