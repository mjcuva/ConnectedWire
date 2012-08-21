from blog.models import Post
from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime

template_vars = {}

def feedBurn(request):
    """
    returns an XML of the most latest posts
    """
    template_vars['posts'] = Post.objects.all().order_by('-published')[:30]
    template_vars['now'] = datetime.datetime.now()

    t = 'feed.xml'


    return render_to_response(t, template_vars, mimetype="text/xml")