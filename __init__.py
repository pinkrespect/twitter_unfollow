from secret import CKEY, CSECRET, ATOKEN, ASECRET
from tweepy import OAuthHandler
import time
import tweepy

auth = OAuthHandler(CKEY, CSECRET)
auth.set_access_token(ATOKEN, ASECRET)
api = tweepy.API(auth)
ME = api.me().screen_name.lower()

mentions = []
friends = []


def duplicate_remove(origin):
    return list(set(origin))


# rate limit handler - tweepy code snippets
def limit_handled(cursor, origin):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print("Rate Limit: sleep 15 minutes")
            print(origin)
            time.sleep(15 * 60)


def load_list(origin):
    global mentions
    global friends
    if origin is friends:
        print("friends process")
        for temp in limit_handled(tweepy.Cursor(api.friends,
                                                screen_name=ME).items(),
                                  origin):
            origin.append(temp.users.screen_name)
    elif origin is mentions:
        print("mentions process")
        for temp in limit_handled(tweepy.Cursor(api.search,
                                                q='to:'+ME).items(),
                                  origin):
            origin.append(temp.screen_name)

    origin = duplicate_remove(origin)
    origin.sort()
    print(origin)
    return origin


friends = load_list(friends)
print(friends)

friends = load_list(mentions)
print(mentions)

