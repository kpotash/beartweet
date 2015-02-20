#!/usr/bin/python

import twitter 
import random
import time
import datetime

import getopt

import sys

#========================================
# example using tweepy, but this did not work on my rpi
#from __future__ import absolute_import, print_function

# # == OAuth Authentication ==
# #
# # This mode of authentication is the new preferred way
# # of authenticating with Twitter.

# # The consumer keys can be found on your application's Details
# # page located at https://dev.twitter.com/apps (under "OAuth settings")
# consumer_key="azFYdj8hnnxCi2n4iVycGSpJW"
# consumer_secret="sWYiBvm6oCGO2r1un2OfvmdDjzRwaIk2Z25vbMCe0oyY6oydsd"

# # The access tokens can be found on your applications's Details
# # page located at https://dev.twitter.com/apps (located
# # under "Your access token")
# access_token="3027469197-PYRRN73BN2pbCsVDAsDxJMYdRDGiD8wAad92YzH"
# access_token_secret="qgMb0blpebIXdTwGOou1g29I6S0vutJ5Pu1X7WWhlz6Pg"

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.secure = True
# auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)

# # If the authentication was successful, you should
# # see the name of the account print out
# print(api.me().name)

# # If the application settings are set for "Read and Write" then
# # this line should tweet out the message to your account's
# # timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
# #api.update_status(status='#H4EAD #H4EADFEB Please lets do this today!')
# #api.update_status('#H4EAD #H4EADFEB Please lets do this today!', media_ids=None)
#========================================

#========================================
# The following sends tweets with a variable frequency
# THANDLES - target twitter handles
# PICS - pic urls that you want to embed in your tweets
# run it as -
# h4ead2.py -k <keys_file> -t <tweets_file> -s <sleep_time_seconds> -d <random_delay_time_seconds>
#
# sample keys_file(get this from twitter app details page) -
#
# consumer_key=xxx
# consumer_secret=xxx
# access_token=xxx
# access_token_secret=xxx
#
# tweets_file -
#
# #H4EADNOW plz approve #H4EAD with immediate effect
# #H4EADNOW plz pass #H4EAD with immediate effect
# #H4EADNOW please approve #H4EAD with immediate effect
# #H4EADNOW please pass #H4EAD with immediate effect
# #H4EADNOW plz approve now #H4EAD with immediate effect
# #H4EADNOW please approve now #H4EAD with immediate effect
# #H4EADNOW please pass now #H4EAD with immediate effect
# #H4EADNOW plz pass now #H4EAD with immediate effect
#
#========================================


STR_KEY_GEN = ' ."\',-:;/=*!^%()[]{}`~$_+|\\'
THANDLES = [ "@WhiteHouse", "@BarackObama", "@OMBPress", "@USCIS"
             # , "@OCRLeon", "@ShaunOMB", "@DeeseOMB", "@MelanieOMB"
             # , "@h4visaacurse", "@USCIS", "@DHSgov"
             ]
PICS = [
    'pic.twitter.com/0keVWC6Clw'
    , 'pic.twitter.com/1sPUUP3wMt'
    , 'pic.twitter.com/WKm3Y0cw3V'
    , 'pic.twitter.com/HpBZVrjLre'
    , 'pic.twitter.com/DoLPHvOPiT'
    , 'pic.twitter.com/B1J1F9tqLx'
    , 'pic.twitter.com/QRROw5ykbf'
    , 'pic.twitter.com/BoknrIKldX'
    , 'pic.twitter.com/F6nlNVckZi'
    , 'pic.twitter.com/0J18gwVj3I'
    , 'pic.twitter.com/u6XOqQ6cnc'
    , 'pic.twitter.com/kBOWdJk4jS'
    , 'pic.twitter.com/rTu0v9nuVH'
    , 'pic.twitter.com/1zfI4Ym8hg'
    , 'pic.twitter.com/7Rxfu3r0k2'
    , 'pic.twitter.com/gsg5cxJII7'
    , 'pic.twitter.com/ZrM4gbNSXV'
    , 'pic.twitter.com/LFhMVFKa0T'
    , 'pic.twitter.com/axqzWxY4od'
    , 'pic.twitter.com/QFSNbFyxNO'
    , 'pic.twitter.com/L68I3WSWC8'
    , 'pic.twitter.com/y3pvfyRw2l'
    , 'pic.twitter.com/M6KxubLL61'
    , 'pic.twitter.com/zfeoCX27YC'
    , 'pic.twitter.com/KaiWS4YvUE'
    , 'pic.twitter.com/lyEHkWwvUP'
    , 'pic.twitter.com/hsUehrg4Ha'
    , 'pic.twitter.com/unqZMIMFI2'
    , 'pic.twitter.com/p6gkmwDLRe'
    , 'pic.twitter.com/MVc6nZZgRS'
    , 'pic.twitter.com/K8g6x9tlDp'
    ]

def generate_key():
    handles = ' '.join(random.sample(THANDLES, 4))
    return ' ' + handles + ' ' + random.choice(PICS) + ' ' + ''.join(random.choice(STR_KEY_GEN) for _ in xrange(5))

def modifyLine(line, sentTweets):
    kline = line.rstrip()
    for _ in range(10):
        kline = kline + generate_key()
        kline = kline[:140]
        
        if kline in sentTweets:
            continue
        else:
            return kline

    return None

def runtweets(api, tweets, sleep, delay):
    sentTweets = set([])
    lastResetTime = datetime.datetime.now()
    while True:
        nowTime = datetime.datetime.now()
        runTime = nowTime - lastResetTime
        if runTime.total_seconds() > 24*60*60:
            lastResetTime = nowTime
            sentTweets.clear()
            print 'reset sentTweets'

        for line in tweets:
            if not line:
                continue
            time.sleep(sleep + random.randint(0, delay))
            tweetLine = modifyLine(line, sentTweets)
            if tweetLine:
                try:
                    api.PostUpdate(tweetLine)
                    print tweetLine
                    sentTweets.add(tweetLine)
                except Exception, e:
                    print "caught an exception: {0}".format(e)
                    
                sys.stdout.flush()


if "__main__" == __name__:

    # print sys.argv[1:]
    optlist, args = getopt.getopt(sys.argv[1:], 'k:t:s:d:') # keys, tweets, sleep, delay
    optdict = dict(optlist)
    print optdict

    key_dict = {}
    # read in keys
    kfile = open(optdict["-k"], 'r')
    for line in kfile:
        kv_splits = line.split("=")
        key_dict[kv_splits[0]] = kv_splits[1].rstrip()
    
    print key_dict

    tweets = []
    # read in tweets
    tfile = open(optdict["-t"], 'r')
    tweets = tfile.read().split("\n")
        
    print tweets

    # initialize api
    api = twitter.Api(consumer_key=key_dict['consumer_key'],
                      consumer_secret=key_dict['consumer_secret'],
                      access_token_key=key_dict['access_token'],
                      access_token_secret=key_dict['access_token_secret'])
    print api.VerifyCredentials()

    # start tweeting
    runtweets(api, tweets, int(optdict['-s']), int(optdict['-d']))
    

