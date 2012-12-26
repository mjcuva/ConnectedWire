import json

from blog.models import Post
from django.http import HttpResponse

def indexJson(request, posts):
    JSON = []

    if not posts:
        posts = 0
    else:
        posts = int(posts)

    posts = Post.objects.all().order_by('-published')[posts:posts+30]

    postid = 0

    for i in posts:
        jsonAddition = {postid: {'title': i.title, 'content': i.content, 'image': i.image, 'source': i.sourceUrl, 'permalink': i.link}}
        JSON.append(jsonAddition)
        postid += 1

    return HttpResponse(json.dumps(JSON), mimetype="application/json")