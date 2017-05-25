import time
import tweepy
import influence_finder as finder


def find_followee_list(screen_name):
    # getting global variables (path, api etc)
    finder.get_variables()
    followee_list = []
    print("Finding followees...")
    # finding all followees
    followees = tweepy.Cursor(finder.api.friends, screen_name=screen_name, count=200).items()
    while True:
        try:
            # reading each followee from iterable 'followees' object
           followee = next(followees)
        except tweepy.TweepError as e:
            if "Connection broken" in str(e):
                print("Error message: "+str(e))
                print("Trying again")
                continue
            elif "Connection aborted" in str(e):
                print("Error message: "+str(e))
                print("Trying again")
                continue
            else:
                print("Error message: "+str(e))
                print('RATE LIMIT - waiting 15 minute...')
                time.sleep(60*15)
                continue
        except StopIteration:
            break
        # adding each followee to followee_list
        followee_list += [followee.screen_name]
    return followee_list
