from django.core.management import setup_environ
from ConnectedWire import settings



setup_environ(settings)

from blog.models import Post


posts = Post.objects.all()

wordcount = 0

for i in posts:

	wordcount += len(i.content.split(' '))

print wordcount