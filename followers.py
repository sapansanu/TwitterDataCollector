import time
import tweepy
import influence_finder as finder


def find_follower_list(screen_name):
    # getting global variables (path, api etc)
    finder.get_variables()
    follower_list = []
    print("Finding followers...")
    # finding all followers
    followers = tweepy.Cursor(finder.api.followers, screen_name=screen_name, count=200).items()
    while True:
        try:
            # reading each follower from iterable 'followers' object
            follower = next(followers)
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
        # adding each follower to follower_list
        follower_list += [follower.screen_name]
    return follower_list
