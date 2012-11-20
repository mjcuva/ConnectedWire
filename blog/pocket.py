# Allows the page to be rendered
from django.http import HttpResponse, HttpResponseRedirect

# Excpetion for objects that don't exist in the database
from django.core.exceptions import ObjectDoesNotExist

# Import database model
from models import PocketKey

# Check if in debug mode
from django.conf import settings

# Makes requests to pocket
import urllib, urllib2

# Utility Functions
import util

# Reads JSON
import json

import secret


CONSUMER_KEY =  secret.POCKET_KEY
url1 = 'https://getpocket.com/v3/oauth/request'
url2 = 'https://getpocket.com/v3/oauth/authorize'
retrieveUrl = 'https://getpocket.com/v3/get'

def getPath():

    if settings.DEBUG == True:
        redirectURL = 'http://localhost:8000'
    else:
        redirectURL = 'http://www.theconnectedwire.com'

    return redirectURL


def checkAuthorized(request):
    user = util.checkLoggedIn(request)

    if user:
        try: 
            key = PocketKey.objects.get(User = user)

            return HttpResponse('True')

        except ObjectDoesNotExist:

            return HttpResponse('False')

    else:
        return HttpResponseRedirect('/')


def authorize(request):

    user = util.checkLoggedIn(request)

    if user:
        try:
            key = PocketKey.objects.get(User = user)

            return HttpResponse('Already Authorized')

        except ObjectDoesNotExist:

            requestToken = getRequestToken()

            redirectURL = getPath()

            url = 'https://getpocket.com/auth/authorize?request_token=' + requestToken + '&redirect_uri=' + redirectURL + '/pocket/approved?request_token=' + requestToken

            return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect("/")


def getRequestToken():

    redirectURL = getPath()

    redirect_uri = redirectURL + '/dashboard'

    values = {
        "consumer_key": CONSUMER_KEY,
        'redirect_uri': redirect_uri
    }

    data = urllib.urlencode(values)
    req = urllib2.Request(url1, data)
    response = urllib2.urlopen(req)

    the_page = response.read()
    code = the_page[(the_page.find('=')) + 1:]
    
    return code

def approved(request):

    user = util.checkLoggedIn(request)

    if user:

        requestToken = request.GET.get('request_token')

        access_token = getAuthorization(requestToken)

        

        key = PocketKey(User = user, key = access_token)
        key.save()

        return HttpResponseRedirect('/dashboard')

    else:

        return HttpResponseRedirect('/')
    

def getAuthorization(requestToken):
    values = {
        'consumer_key': CONSUMER_KEY,
        'code': requestToken
    }

    data = urllib.urlencode(values)
    req = urllib2.Request(url2, data)

    response = urllib2.urlopen(req)

    the_page = response.read()

    access_token = the_page[(the_page.find('access_token=')) + 13:(the_page.find('&'))]

    return access_token

    
def getArticles(request):

    user = util.checkLoggedIn(request)

    if user:

        access_token = PocketKey.objects.get(User = user).key

        values = {
            'consumer_key': CONSUMER_KEY,
            'access_token': access_token
        }

        data = urllib.urlencode(values)
        req = urllib2.Request(retrieveUrl, data)

        response = urllib2.urlopen(req)

        data = json.loads(response.read())

        
        outputlist = []
        

        for i in data["list"]:
            output = {'output': '', 'added': ''}
            k = 0
            inserted = False
            title = data['list'][i]['resolved_title']
            url = data['list'][i]['resolved_url']
            excerpt = data['list'][i]['excerpt']
            output['output'] = '<a class="starredLink" target="_blank" href="' + url + '"><div class="starredItem">' + title + '<div class="excerpt"> - ' + excerpt + '</div></div></a>'
            output['added'] = data['list'][i]['time_added']
            while(k < len(outputlist)):

                if outputlist[k]['added'] >= output['added']:
                    k += 1
                else:
                    # print output
                    outputlist.insert(k, output)
                    inserted = True
                    break

            if inserted == False:
                # print output
                outputlist.append(output)

        outputString = ''

        # print outputlist

        for j in outputlist:
            # print j
            outputString += j['output']


        return HttpResponse(outputString)

    else:

        return 'Not Logged In'
