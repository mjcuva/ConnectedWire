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