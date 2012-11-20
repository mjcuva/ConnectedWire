# Allows the page to be rendered
from django.shortcuts import render_to_response

# Allows redirects, as well as 404 pages
from django.http import HttpResponseRedirect, Http404, HttpResponse

# Allows the request to be sent to the template
from django.template import RequestContext

import util

# Calculate stats about posts for dashboard
import stats

from models import Todo


# Displays the dashboard
def dash(request):

	# Gets the logged in user, or redirects
	username = util.checkLoggedIn(request)
	if not username:
		return HttpResponseRedirect('/login?next=dashboard')

	# Gets total wordcount
	wordCountInt, wordCountString = stats.getWordCount()

	# Gets total number of posts
	postCount = stats.getPostCount()

	average = int(int(wordCountInt) / int(postCount));

	# Days since last post
	daysSince = stats.daysSince()

	# Makes sure the grammar is correct
	if not daysSince == 1:
		day = "days"
	else:
		day = 'day'

	# Gets the top story title and link from techmeme
	suggestionTitle, suggestionLink = stats.suggestion()

	todo = Todo.objects.all().order_by('-id')

	# Renders the dashboard html page
	return render_to_response("dashboard/main.html", {'username':username,
														'wordCountString': wordCountString,
														'average': average,
														'postCount': postCount,
														'daysSince':daysSince,
														'day': day,
														'suggestionTitle':suggestionTitle,
														'suggestionLink':suggestionLink,
														'todo': todo}, context_instance =RequestContext(request))


def addTodo(request):

	todoText = request.GET.get('item')

	todo = Todo(text = todoText)

	todo.save()

	return render_to_response('dashboard/todo.html', {'todoItem':todo}, context_instance =RequestContext(request))


def deleteTodo(request):

	itemid = request.GET.get('id')

	item = Todo.objects.get(pk = itemid)

	item.delete()

	return HttpResponse('deleted')