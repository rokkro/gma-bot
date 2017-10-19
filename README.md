# gma-bot

How it works:

Grandma bot will use a random term from bot_focus.txt and use Tweepy's streaming client to get a (new) tweet. Links, '#', and '@' are removed.

The bot will then use the stanford parser, and deconstruct the tweet. It will obtain the nouns, verbs, adjectives, and adverbs.

A noun, verb, adj, and adv will be picked randomly. NLTK will find a list of synonyms of the noun and verb.

A random noun synonym and verb synonym will be selected and made plural using the `inflect` package. 

The bot will re-assemble a sentence like so: 

[random intro text] [adverb] [verb] [adjective] [# (50% chance of this appearing)] [noun] [random ending text].


The new tweet will be tweeted every 5 minutes to 4 hours.


This bot cannot reply to the original tweet because of Twitter's rules.

