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

from django.db import models

CATEGORIES = (('News','News'),('Editorial','Editorial'), ('Rumor','Rumor'), ('Google', 'Google'), ('Apple', 'Apple'), ('Microsoft', 'Microsoft'), ('Favorites', 'Favorites'))

class Post(models.Model):
	title = models.CharField(max_length = 100)
	content = models.TextField()
	published = models.DateTimeField()
	link = models.CharField(max_length = 100)
	sourceUrl = models.CharField(max_length = 100, blank = True, null = True)
	image = models.CharField(max_length = 100, blank = True, null = True)
	
	
	def __unicode__(self):
		return self.title
		
class User(models.Model):
	username = models.CharField(max_length = 10)
	password = models.CharField(max_length = 100)
	
	def __unicode__(self):
		return self.username

class Categories(models.Model):
	Post = models.ForeignKey(Post)
	category = models.CharField(max_length = 100, blank = True, null = True)

	def __unicode__(self):
		return self.category

class Page(models.Model):
	title = models.CharField(max_length = 10)
	content = models.TextField()
	image = models.CharField(max_length = 100, blank = True, null = True)

	def __unicode__(self):
		return self.title


class Featured(models.Model):
	Post = models.ForeignKey(Post, null = True, blank = True)
	box = models.IntegerField()
	imageURL = models.TextField()

	def __unicode__(self):
		return self.Post.title





