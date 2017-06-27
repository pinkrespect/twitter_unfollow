from secret import CKEY, CSECRET, ATOKEN, ASECRET
from tweepy import OAuthHandler
import time
import tweepy

auth = OAuthHandler(CKEY, CSECRET)
auth.set_access_token(ATOKEN, ASECRET)
api = tweepy.API(auth)
ME = api.me().screen_name.lower()


# rate limit handler - tweepy code snippets
def limit_handled(cursor, origin_set):
    while True:
        try:
            yield cursor.next()

        except tweepy.RateLimitError:
            print("size of list", len(origin_set))
            time.sleep(15 * 60)


def load_friends():
    friends = set()
    for temp in limit_handled(tweepy.Cursor(api.friends,
                                            screen_name=ME).items(),
                              friends):
        friends.add(temp.screen_name)
    return friends


def load_mentions():
    mentions = set()
    for temp in limit_handled(tweepy.Cursor(api.friends,
                                            screen_name=ME).items(),
                              mentions):
        mentions.add(temp.screen_name)
    return mentions


friends = load_friends()
print(" size of friends: ", len(friends))

mentions = load_mentions()
print(" size of mentions: ", len(mentions))

unfollow_list = list(friends - mentions)
print(" unfollow list: ", unfollow_list)
