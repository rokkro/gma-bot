from os.path import dirname,abspath
from text_parse import form_phrase
from twitter import stream, tweet_status
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
    print(ending)
    text = text_content
    result = form_phrase(intro, text, ending, check_words=True, capitalized=random.choice([True,False]), extras=False)
    return result

def get_a_tweet():
    while True:
        search = random.choice(get_lines("bot_focus.txt"))
        if not search:
            continue
        print(search)
        tweet = stream([search],[])
        tweet_text = tweet['text']
        tweet_text = tweet_text.replace("@","").replace("#","").replace("\n","")
        tweet_text = re.sub(r"http\S+", "", tweet_text)

        print(tweet_text)
        try:
            result = text_get(tweet_text)
            print(result)
        except UnicodeEncodeError as e:
            print(e)
            continue
        if result is None:
            continue
        else:
            result = result.replace("n't","")
            tweet_status(result, search)
            sleep_time = random.choice(range(300,14400))
            print("Sleeping for",sleep_time)
            sleep(sleep_time)

get_a_tweet()
