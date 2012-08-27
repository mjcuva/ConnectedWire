# dashboard.py
# ------------
# Renders the dashboard page.
# 
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.



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
		return HttpResponseRedirect('/')

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