import json
import os
import time
import tweepy
import followers as fr
import followees as fe


# AUTHENTICATION (OAuth)
def authorize(authfile):
    with open(authfile, "r") as f:
        ak = f.readlines()
    f.close()
    auth1 = tweepy.auth.OAuthHandler(ak[0].replace("\n", ""), ak[1].replace("\n", ""))
    auth1.set_access_token(ak[2].replace("\n", ""), ak[3].replace("\n", ""))
    return tweepy.API(auth1)


def search_tweets(word, c):
    for tweet in tweepy.Cursor(api.search, q=word, lang="en", count=c).items(c):
        data = {}
        data['user_id'] = tweet.author.id   # author/user ID#
        data['screen_name'] = tweet.author.screen_name
        data['followers_count'] = tweet.author.followers_count      # number of author/user followers
        data['followees_count'] = tweet.author.friends_count    # number of author/user friends
        data['verified'] = tweet.author.verified
        data['account_created_at'] = str(tweet.author.created_at)       # account age
        data['average_retweet_count'] = 0       # average retweet count based on original tweets
        data['average_favorite_count'] = 0      # average favorite count based on original tweets
        data['total_tweets'] = 0    # total number of tweets read by program
        data['retweets'] = 0        # number of retweets among total_tweets (orignal tweets = total_tweets - retweets)
        data['retweeted_by_others'] = 0     # number of original tweets retweeted by others
        data['mentioned_others'] = 0    # number of times current user mentioned others
        data['tweets'] = []     # all tweets read
        data['tweet_created_at'] = []       # time each read tweet was created at
        data['followers_list'] = []     # list of users that follow current user
        data['followees_list'] = []     # list users that current user follows
        # getting user account details
        get_user_profile(data)


def get_user_profile(data):
    global api, path
    total_retweet= 0
    total_favourite = 0
    total_tweets  = 0
    original_tweets = 0
    screen_name = data['screen_name']
    try:
        # getting tweets from user timeline
        timeline = api.user_timeline(screen_name, count=200)
    except tweepy.TweepError as e:
        if "Connection broken" in str(e):
            print("Error message: "+str(e))
            print("Trying again")
            return
        elif "Connection aborted" in str(e):
            print("Error message: "+str(e))
            print("Trying again")
            return
        else:
            print("Error message: "+str(e))
            print('RATE LIMIT - waiting 15 minutes...')
            time.sleep(60*15)
            return
    for tweet in timeline:
        # reading each tweet
        print("Reading tweet : "+tweet.text)
        data['tweets'] += [tweet.text]
        data['tweet_created_at'] += [str(tweet.created_at)]
        total_tweets += 1
        # checking if tweet is a retweet (or not original)
        if "RT @" in tweet.text:
            data['retweets'] += 1
        else:
            # storing attributes for original tweets
            total_retweet += tweet.retweet_count
            total_favourite += tweet.favorite_count
            original_tweets += 1
            # checking if tweet was retweeted by followers
            if tweet.retweet_count>0:
                data['retweeted_by_others'] += 1
            # checking if current user mentioned any other user in current tweet
            if "@" in tweet.text:
                data['mentioned_others'] += 1
    print("Total tweets by "+screen_name+" : "+str(total_tweets))
    print("Original tweets by "+screen_name+" : "+str(original_tweets))
    # calculating average scores for original tweets
    if original_tweets > 0:
        data['average_retweet_count'] = round(total_retweet/original_tweets, 2)
        data['average_favorite_count'] = round(total_favourite/original_tweets, 2)
    data['total_tweets'] = total_tweets
    # finding followers list
    follower_list = fr.find_follower_list(screen_name)
    data['followers_list'] = follower_list
    # finding followees list
    followee_list = fe.find_followee_list(screen_name)
    data['followees_list'] = followee_list
    # writing json file
    write_json(screen_name, data, path)


def write_json(screen_name, data, write_path):
    print("Write path :"+str(write_path))
    if not os.path.exists(write_path):
        os.makedirs(write_path)
    file = open(write_path+screen_name+".json","w")
    json.dump(data,file, indent=4)
    file.close()
    print("Writen : "+str(screen_name))


def get_variables():
    global api, path
    path = "./real_users/"
    # OAuth key file
    authfile = './auth.k'
    api = authorize(authfile)


# MAIN ROUTINE
def main():
    global bag_of_words
    # setting global variables
    get_variables()
    # array containing keywords to use for searching tweets
    bag_of_words = ['Credit card OR credit card']

    for word in bag_of_words:
        search_tweets(word, 100)


if __name__ == "__main__":
    main()
