# Allows the page to be rendered
from django.shortcuts import render_to_response

# Allows redirects, as well as 404 pages
from django.http import HttpResponseRedirect, Http404

# Allows the request to be sent to the template
from django.template import RequestContext

import util

# Calculate stats about posts for dashboard
import stats


# Displays the dashboard
def dash(request):

	# Gets the logged in user, or redirects
	username = util.checkLoggedIn(request)
	if not username:
		return HttpResponseRedirect('/login')

	# Gets total wordcount
	wordCount = stats.getWordCount()

	# Gets total number of posts
	postCount = stats.getPostCount()

	# Days since last post
	daysSince = stats.daysSince()

	# Makes sure the grammar is correct
	if not daysSince == 1:
		day = "days"
	else:
		day = 'day'

	# Gets the top story title and link from techmeme
	suggestionTitle, suggestionLink = stats.suggestion()

	# Renders the dashboard html page
	return render_to_response("dashboard/index.html", {'username':username,
														'wordCount': wordCount,
														'postCount': postCount,
														'daysSince':daysSince,
														'day': day,
														'suggestionTitle':suggestionTitle,
														'suggestionLink':suggestionLink}, context_instance =RequestContext(request))