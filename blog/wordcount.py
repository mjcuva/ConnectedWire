from blog.models import Post

def getWordCount():
	posts = Post.objects.all()

	wordcount = 0

	for i in posts:

		wordcount += len(i.content.split(' '))

	return wordcount
