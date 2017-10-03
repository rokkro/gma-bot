from os.path import dirname,abspath
from src.text_parse import form_phrase
from src.twitter import stream, tweet_status
import re
import random
from time import sleep

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
    return result

def get_a_tweet():
    while True:
        search = random.choice(get_lines("bot_focus.txt"))
        print(search)
        tweet = stream([search],[])
        tweet_id = tweet['id']
        tweet_text = tweet['text']
        tweet_user = tweet['user']['screen_name']
        tweet_text = tweet_text.replace("@","").replace("#","").replace("\n","")
        tweet_text = re.sub(r"http\S+", "", tweet_text)

        print(tweet_text)
        result = text_get(tweet_text)
        print(result)
        if result is None:
            sleep(5)
        else:
            tweet_status(result, search)
            sleep(1800)


get_a_tweet()
