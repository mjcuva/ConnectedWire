# -*- coding: utf-8 -*-

from xml.dom.minidom import parse
from datetime import datetime
import time
from blog.models import Post, Categories
from django.http import HttpResponseRedirect



CATLIST = ['News', 'Editorial', 'Rumor', 'Google', 'Apple', 'Microsoft']

def splice(item, startString, endString):
	start = item.find(startString) + len(startString)
	end = item.find(endString)
	return item[start:end]

def remove(item, startString, endString):
	start = item.find(startString)
	end = item.find(endString, start + len(startString)) + len(endString)
	item = item[:start] + item[end:]
	return item




def importer(request):

	dom = parse('/Users/Marc/Downloads/connectedwire.xml')

	posts = dom.getElementsByTagName('item')


	for post in posts:

		title = post.getElementsByTagName('title')[0]

		title = title.toxml()
		title = splice(title, '<title>', "</title>")

		# print title


		content = post.getElementsByTagName('content:encoded')[0]

		content = content.toxml()
		content = splice(content, '<content:encoded>', '</content:encoded>')

		content = remove(content, '<img', '/>')

		endCaption = content.find("[/caption]") + len('[/caption]')

		if endCaption != (9):
			content = content[endCaption:]

		gallery = content.find('[gallery link')

		if gallery != -1:
			content = remove(content, '[gallery ', '"]')

		content = content.replace(']]>', "")
		# content = remove(content, ']', '>')
		content = remove(content, '<!', '</a>')
		content = content.encode('ascii', 'xmlcharrefreplace')
		content = "<br />".join(content.split('\n'))

		# print '\n'
		# print content

		categories = post.getElementsByTagName('category')

		cats = []

		for i in categories:
			cat = i.toxml()
			cat = remove(cat, '<category','[CDATA[')
			cat = remove(cat, ']]', '</category>')
			if cat in CATLIST and cat not in cats:
				# print cat
				cats.append(cat)

		published = post.getElementsByTagName('wp:post_date')[0]
		published = published.toxml()
		published = splice(published, '<wp:post_date>', '</wp:post_date>')
		published = datetime.fromtimestamp(time.mktime(time.strptime(published, "%Y-%m-%d %H:%M:%S")))


		post = Post(title = title, 
								content = content, 
								published = published,
								link = str(published.day) + '/' + title[:5])
		post.save()

		for category in cats:
			newCategory = Categories(Post = post, category = category)
			newCategory.save()

		

	return HttpResponseRedirect('/')


