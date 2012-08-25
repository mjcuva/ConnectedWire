#Allows the page to be rendered
from django.shortcuts import render_to_response

# Allows redirects, as well as 404 pages
from django.http import HttpResponseRedirect, Http404

import util
import stats

def dash(request):
	username = util.checkLoggedIn(request)
	if not username:
		return HttpResponseRedirect('/')

	wordCount = stats.getWordCount()
	postCount = stats.getPostCount()
	daysSince = stats.daysSince()

	if daysSince > 1:
		day = "days"
	else:
		day = 'day'

	suggestionTitle, suggestionLink = stats.suggestion()

	return render_to_response("dashboard/index.html", {'username':username,
														'wordCount': wordCount,
														'postCount': postCount,
														'daysSince':daysSince,
														'day': day,
														'suggestionTitle':suggestionTitle,
														'suggestionLink':suggestionLink})