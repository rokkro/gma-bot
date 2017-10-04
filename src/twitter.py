try:
    from config import config
    import tweepy, json
    from time import sleep
    from tweepy import Stream
    from tweepy.streaming import StreamListener
    from tweepy import OAuthHandler
except ImportError as e:
    print("Import Error in stream.py:", e)
    quit()

auth = tweepy.OAuthHandler(config['TWITTER']['ckey'], config['TWITTER']['csecret'])
auth.set_access_token(config['TWITTER']['atoken'],config['TWITTER']['asecret'])

#Initialize tweepy api with authentication keys
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

class Listener(StreamListener):
    # Override Tweepy's Listener class, on_data and on_error
    def __init__(self):
        super().__init__()
        self.tweet = None

    def on_data(self, data):
        # Manage retrieved json doc
        json_data = json.loads(data)
        if "created_at" not in json_data or "retweeted_status" in json_data or \
                        "quoted_status" in json_data or json_data["in_reply_to_user_id"] != None:
            return
        else:
            self.tweet = json_data
            raise KeyboardInterrupt

    def on_error(self, status):
        # Handle error codes
        if status == 420:
            raise Exception("Rate limit reached. Please try again later.")
        if status == 406:
            raise Exception("Invalid tweet search request.")
        if status == 401:
            raise Exception("Authentication failed. Check your keys and verify your system clock is accurate.")
        raise Exception("ERROR CODE",status)


def stream(terms, user):
    listener = None
    while True:  # start streaming
        try:
            listener = Listener()
            twitter_stream = Stream(auth, listener)
            print(terms)
            twitter_stream.filter(track=terms, follow=user, languages=['en'])
        except KeyboardInterrupt:
            return listener.tweet
        except Exception as e:
            print("Error: ",e," Attempting to continue...",end='')
            continue

def tweet_status(content,hashtag):
    api.update_status(content)