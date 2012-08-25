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

from blog.models import Post
import datetime
from bs4 import BeautifulSoup
import urllib2

def getWordCount():
	posts = Post.objects.all()

	wordcount = 0

	for i in posts:

		wordcount += len(i.content.split(' '))

	wordcount = format(wordcount, ",d")

	return wordcount

def getPostCount():
	posts = Post.objects.all()

	postcount = len(posts)

	return postcount

def daysSince():
	last = Post.objects.all().order_by('-published')[0].published.replace(tzinfo=None)
	now = datetime.datetime.now()
	delta = now - last
	return delta.days

def suggestion():
	page = urllib2.urlopen('http://techmeme.com').read()
	soup = BeautifulSoup(page)

	topItem = soup.find('strong').contents


	firstLinkChar = str(topItem).find('href="') + 6

	newlink = str(topItem)[firstLinkChar:]

	lastLinkChar = newlink.find('"')

	link = newlink[:lastLinkChar]

	title = topItem[0].contents[0]

	title = title.encode('ascii')

	return title, link









