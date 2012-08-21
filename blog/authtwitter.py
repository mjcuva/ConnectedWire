import tweepy

CONSUMER_KEY = 'LsMrljvjXYYe82of32C2A'
CONSUMER_SECRET = 'xdHu005Yte39RJqITV9ux3YphSJOe05GPXYfHHOm8'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth_url = auth.get_authorization_url()
print 'Please authorize: ' + auth_url
verifier = raw_input('PIN: ').strip()
auth.get_access_token(verifier)
print "ACCESS_KEY = '%s'" % auth.access_token.key
print "ACCESS_SECRET = '%s'" % auth.access_token.secret