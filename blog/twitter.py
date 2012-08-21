import sys
import tweepy
import ConnectedWire.settings

CONSUMER_KEY = 'LsMrljvjXYYe82of32C2A'
CONSUMER_SECRET = 'xdHu005Yte39RJqITV9ux3YphSJOe05GPXYfHHOm8'
ACCESS_KEY = '48885048-T1o6vVa4mIx6O8xVAJeU3hdUSQzfIyrO53pjVDoIK'
ACCESS_SECRET = 'pW2lmSoqAF33j2o3ducX9zp4BseJ6xwuGTGO8Xx0'


def updateTwitter(tweet):
	if not ConnectedWire.settings.DEBUG:
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		api = tweepy.API(auth)
		api.update_status(tweet)
		return True
	return False