# Allows the page to be rendered
from django.shortcuts import render_to_response

from django.http import HttpResponseRedirect

import util

import blogForms

import datetime

from django.core.files.storage import FileSystemStorage

import paths

import os

# Allows the request to be sent to the template
from django.template import RequestContext

from models import Podcast, Page

def addEpisode(request):

    username = util.checkLoggedIn(request)
    if not username:
        return HttpResponseRedirect('/')
    error = ""

    if request.method == "POST":

        form = blogForms.newEpisodeForm(request.POST)

        title = request.POST['title']

        showNotes = request.POST['showNotes']

        episodeURL = '/podcasts/' + request.POST['episode']

        size = request.POST['length']

        if title and showNotes and episodeURL and size:

            published = datetime.datetime.now()

            if 'image' in request.FILES:

                image = request.FILES['image']

                store = FileSystemStorage(paths.SITE_ROOT + '/images/')

                storedImage = store.save(image.name, image)

                imageURL = '/images/' + storedImage

            else:

                imageURL = None

            episode = Podcast(title = title, 
                              link = episodeURL, 
                              showNotes = showNotes, 
                              length = size, 
                              date = published,
                              imageURL = imageURL)
            episode.save()

            return HttpResponseRedirect('/podcast')

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


def showEpisodes(request):

    username = util.checkLoggedIn(request)

    podcasts = Podcast.objects.all().order_by('-date')

    pages = Page.objects.all().order_by('id')

    return render_to_response("podcasts.html", {"podcasts": podcasts, "pages": pages, "username":username})

def deleteEpisode(request, id):

    username = util.checkLoggedIn(request)

    if not username:
        return HttpResponseRedirect('/')

    episode = Podcast.objects.get(pk=id)

    try:
        os.remove(paths.SITE_ROOT + episode.link)
        os.remove(paths.SITE_ROOT + episode.imageURL)
    except OSError:
        pass

    episode.delete()

    return HttpResponseRedirect('/podcast')


