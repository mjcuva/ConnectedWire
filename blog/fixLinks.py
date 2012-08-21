from models import Post

posts = Post.objects.all()

for post in posts:

	post.link = post.title.replace(' ', '-')

	post.save()