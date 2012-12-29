# Allows the page to be rendered
from django.shortcuts import render_to_response

from django.http import HttpResponseRedirect

import util

import blogForms

import datetime

from django.core.files.storage import FileSystemStorage

import paths

# Allows the request to be sent to the template
from django.template import RequestContext

from models import Podcast

def addEpisode(request):

    username = util.checkLoggedIn(request)
    if not username:
        return HttpResponseRedirect('/')
    error = ""

    if request.method == "POST":

        form = blogForms.newEpisodeForm(request.POST)

        title = request.POST['title']

        showNotes = request.POST['showNotes']

        if 'episode' in request.FILES and title and showNotes:
           
            episode = request.FILES['episode']

            store = FileSystemStorage(paths.SITE_ROOT + "/podcasts/")

            storedEpisode = store.save(episode.name, episode)

            episodeURL = "/podcasts/" + storedEpisode

            size = store.size(episode.name)

            published = datetime.datetime.now()

            episode = Podcast(title = title, 
                              link = episodeURL, 
                              showNotes = showNotes, 
                              length = size, 
                              date = published)
            episode.save()

            return HttpResponseRedirect('/dashboard')

        else:
            error = "You forgot something"


    else:
        form = blogForms.newEpisodeForm()

    # Renders the dashboard html page
    return render_to_response("dashboard/newEpisode.html", {'username':username, 'form':form, 'error':error}, context_instance =RequestContext(request))


def generateRSS(request):
    
    podcasts = Podcast.objects.all().order_by('-date')

    lastepisode = podcasts[0].date

    return render_to_response("podcast.xml", {"podcasts": podcasts, 'lastepisode': lastepisode}, mimetype="text/xml")



