'''
Gets text content for tweet IDs
Credit: https://stackoverflow.com/questions/28384588/twitter-api-get-tweets-with-specific-id
'''

# standard
import csv
from __future__ import print_function
import getopt
import logging
import os
import sys
import time
import tweepy

# global logger level is configured in main()
Logger = None

# Generate your own at https://apps.twitter.com/app
CONSUMER_KEY = os.environ['TWITTER_API_KEY']
CONSUMER_SECRET = os.environ['TWITTER_API_SECRET']
OAUTH_TOKEN = os.environ['TWITTER_API_ACCESS_TOKEN']
OAUTH_TOKEN_SECRET = os.environ['TWITTER_API_ACCESS_SECRET']

# batch size depends on Twitter limit, 100 at this time
batch_size=100

def get_tweet_id(line):
    '''
    Extracts and returns tweet ID from a line in the input.
    '''
    return line.split(',')[0]

def get_tweets_single(twapi, idfilepath):
    '''
    Fetches content for tweet IDs in a file one at a time,
    which means a ton of HTTPS requests, so NOT recommended.

    `twapi`: Initialized, authorized API object from Tweepy
    `idfilepath`: Path to file containing IDs
    '''
    # process IDs from the file
    with open(idfilepath, 'rb') as idfile:
        for line in idfile:
            tweet_id = get_tweet_id(line)
            Logger.debug('get_tweets_single: fetching tweet for ID %s', tweet_id)
            try:
                tweet = twapi.get_status(tweet_id)
                print('%s,%s' % (tweet_id, tweet.text.encode('UTF-8')))
            except tweepy.TweepError as te:
                Logger.warn('get_tweets_single: failed to get tweet ID %s: %s', tweet_id, te.message)
                # traceback.print_exc(file=sys.stderr)
        # for
    # with

def get_tweet_list(twapi, idlist, writefile):
    '''
    Invokes bulk lookup method.
    Raises an exception if rate limit is exceeded.
    '''
    # fetch as little metadata as possible
    try:
        tweets = twapi.statuses_lookup(id_=idlist, include_entities=False, trim_user=True)
    except tweepy.RateLimitError:
        print("resting...")
        time.sleep(60 * 15)
        tweets = twapi.statuses_lookup(id_=idlist, include_entities=False, trim_user=True)
    if len(idlist) != len(tweets):
        Logger.warn('get_tweet_list: unexpected response size %d, expected %d', len(tweets), len(idlist))
    with open(writefile, 'a+') as f:
        for tweet in tweets:
            writer = csv.writer(f, delimiter=',')
            writer.writerow([tweet.id, tweet.text.encode('UTF-8')])

            # f.write('%s,,%s,,' % (tweet.id, tweet.text.encode('UTF-8')))

def get_tweets_bulk(twapi, idfilepath, writefile):
    '''
    Fetches content for tweet IDs in a file using bulk request method,
    which vastly reduces number of HTTPS requests compared to above;
    however, it does not warn about IDs that yield no tweet.

    `twapi`: Initialized, authorized API object from Tweepy
    `idfilepath`: Path to file containing IDs
    '''    
    # process IDs from the file
    tweet_ids = list()
    with open(idfilepath, 'rb') as idfile:
        for line in idfile:
            tweet_id = get_tweet_id(line)
            Logger.debug('Enqueing tweet ID %s', tweet_id)
            tweet_ids.append(tweet_id)
            # API limits batch size
            if len(tweet_ids) == batch_size:
                Logger.debug('get_tweets_bulk: fetching batch of size %d', batch_size)
                get_tweet_list(twapi, tweet_ids, writefile)
                tweet_ids = list()
    # process remainder
    if len(tweet_ids) > 0:
        Logger.debug('get_tweets_bulk: fetching last batch of size %d', len(tweet_ids))
        get_tweet_list(twapi, tweet_ids, writefile)

def usage():
    print('Usage: get_tweets_by_id.py [options] file')
    print('    -s (single) makes one HTTPS request per tweet ID')
    print('    -v (verbose) enables detailed logging')
    sys.exit()

def main(args):
    logging.basicConfig(level=logging.WARN)
    global Logger
    Logger = logging.getLogger('get_tweets_by_id')
    bulk = True
    try:
        opts, args = getopt.getopt(args, 'sv')
    except getopt.GetoptError:
        usage()
    for opt, _optarg in opts:
        if opt in ('-s'):
            bulk = False
        elif opt in ('-v'):
            Logger.setLevel(logging.DEBUG)
            Logger.debug("main: verbose mode on")
        else:
            usage()
    if len(args) != 2:
        usage()
    idfile = args[0]
    writefile = args[1]
    if not os.path.isfile(idfile):
        print('Not found or not a file: %s' % idfile, file=sys.stderr)
        usage()

    # connect to twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    api = tweepy.API(auth)

    # hydrate tweet IDs
    if bulk:
        get_tweets_bulk(api, idfile, writefile)
    else:
        get_tweets_single(api, idfile)

if __name__ == '__main__':
    main(['../data/tweets_raw/tweets.nfl.2010.weekly.csv', '../data/tweets/tweets.nfl.2010.weekly.text.csv'])
    main(['../data/tweets_raw/tweets.nfl.2011.weekly.csv', '../data/tweets/tweets.nfl.2011.weekly.text.csv'])
    main(['../data/tweets_raw/tweets.nfl.2012.weekly.csv', '../data/tweets/tweets.nfl.2012.weekly.text.csv'])



