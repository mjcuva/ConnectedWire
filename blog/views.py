# views.py
# -----------
#
# Controls the majority of the site, including the index,
# new post, new page, pages, categories, archive, and editing.
#
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

# Allows the page to be rendered
from django.shortcuts import render_to_response

# Allows redirects, as well as 404 pages
from django.http import HttpResponseRedirect, Http404, HttpResponse

# Verifies the Token when submitting form
from django.template import RequestContext

#Allows database operations
from models import Post, User, Categories, Page, Featured

# Excpetion for objects that don't exist in the database
from django.core.exceptions import ObjectDoesNotExist

# Uploading images
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import FileSystemStorage

# Pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Utility functions
import util

#Form templates
import blogForms

# PIL Image Library
from PIL import Image

# Time Function
import datetime

# Allows posting to Twitter
import twitter

# Stats for the dashboard
import stats

# OS Paths for files
import paths

# Check if in debug mode
from django.conf import settings

import json


# Homepage
def index(request):

    # Check if user is on IE 8
    ie = False
    if request.META.has_key('HTTP_USER_AGENT'):
        user_agent = request.META['HTTP_USER_AGENT']
        if user_agent.find('MSIE 8.0') != -1:
            ie = True
    
    # Checks if a user is logged in
    username = util.checkLoggedIn(request)
    
    # Queries the database
    posts = Post.objects.all().order_by("-published")
    
    # Gets the templates
    template = "base.html"
    page_template = "index.html"
    
    # If the request is coming from an ajax request
    # and sets the template accordingly
    if request.is_ajax():
        template = page_template
    

    # Get featured posts
    featured = []
    cats = []
    for i in range(0,4):
        try:
            featured.append(Featured.objects.filter().order_by('-Post__published')[i])
            feature = Featured.objects.filter().order_by('-Post__published')[i]
            categories = Categories.objects.filter(Post__title=feature.Post.title)
            added = False
            for i in categories:
                if not (str(i) == 'News' or str(i) == 'Editorial'):
                    cats.append(i)
                    added = True
                    break
                if added:
                    break
            done = False
            if not added:
                for i in categories:
                    if str(i) == 'Editorial':
                        cats.append('Editorial')
                        done = True

                if not done:
                    cats.append('News')

        except IndexError:
            pass

    # dfs
    
    # Gets all of the pages
    pages = Page.objects.all().order_by("id")
    
    # Renders the page
    
    # If on IE, show message asking user to use another broswer
    if not ie:
        return render_to_response(template, {"posts" : posts, "pages":pages, "username": username, "featured": featured, "cats":cats}, context_instance=RequestContext(request))
    else:
        return render_to_response('ie.html')

def indexJson(request, posts):
    JSON = []



    if not posts:
        posts = 0
    else:
        posts = int(posts)

    posts = Post.objects.all().order_by('-published')[posts:posts+30]

    for i in posts:
        jsonAddition = {'title': i.title, 'content': i.content, 'image': i.image, 'source': i.sourceUrl, 'permalink': i.link}
        JSON.append(jsonAddition)

    return HttpResponse(json.dumps(JSON), mimetype="application/json")



# Loads the archive for a specific year
def archive(request, year):
    
    # Gets logged in user
    username = util.checkLoggedIn(request)
    
    # Gets all of the posts
    posts = Post.objects.filter(published__year=year).order_by('-published')
    
    
    # Gets templates and sets appropriate template
    template = "base.html"
    page_template = "index.html"
    
    if request.is_ajax():
        template = page_template
    
    # Loads all pages
    pages = Page.objects.all().order_by("id")
    
    # Renders the page
    if len(posts) > 0:
        return render_to_response(template, {"posts" : posts, "pages":pages, "username": username}, context_instance=RequestContext(request))
    else:
        raise Http404

#Loads the page for a specific category
def category(request, category):
    

    
    username = util.checkLoggedIn(request)
    
    template = "base.html"
    page_template = "index.html"
    
    if request.is_ajax():
        template = page_template
    
    
    posts = []
    catList = Categories.objects.filter(category=category).order_by('-id')
    
    for i in catList:
        posts.append(i.Post)
    
    pages = Page.objects.all().order_by("-id")
    

    
    
    return render_to_response(template, {"posts" : posts, "pages":pages, "username": username}, context_instance=RequestContext(request))


#Creates a new user
def signup(request):
    error = ""
    if request.method == 'POST':
        form = blogForms.SignupForm(request.POST)
        
        #Auth prevents arbitrary users from signing up,
        #guarantees only poeple that wanted to post can create an account
        if form.is_valid() and request.POST['auth'] == 'connectedwiresignup':
            if not util.comparePassword(request.POST['password'], request.POST['verify']):
                error = "Passwords did not match"
            else:
                password = util.make_pw_hash(request.POST['username'], request.POST['password'])
                user = User(username = request.POST['username'], password = password)
                user.save()
                #UID is used to store the user in a cookie
                uid = user.id
                #Gets a hashed value for the user to prevent anyone from setting a cookie and logging in
                val = util.make_secure_val(str(uid))
                response = HttpResponseRedirect('/')
                response.set_cookie("user",val)
                return response
        
        else:
            error = "Invalid Information"
    else:
        form = blogForms.SignupForm()
    
    return render_to_response("signup.html", {"form": form, "error": error}, context_instance=RequestContext(request))

#Logs in a user
def login(request):
    error = ""
    redirect_to = request.REQUEST.get('next', '')
    if request.method == "POST":
        form = blogForms.LoginForm(request.POST)
        if form.is_valid():
            try:
                #Gets the user from the db if it exists
                u = User.objects.get(username=request.POST['username'])
                #Compares password user gave with pass stored in db
                if util.valid_pw(request.POST['username'], request.POST['password'], u.password):
                    #Sets cookie if login is valid
                    uid = u.id
                    val = util.make_secure_val(str(uid))
                    # if request.REQUEST.get('next', ''):
                    if redirect_to:
                        response = HttpResponseRedirect(redirect_to)
                    else:
                        response = HttpResponseRedirect('/')
                    # else:
                    #     response = HttpResponseRedirect('/')
                    response.set_cookie("user",val)
                    return response
            #If the user doesn't exist
            except ObjectDoesNotExist:
                error = "Invalid Login"
            else:
                error = "Invalid Login"
        else:
            error = "Invalid Login"
    else:
        form = blogForms.LoginForm()
    return render_to_response("login.html", {"form": form, "error": error, "redirect_to": redirect_to}, context_instance=RequestContext(request))

#Logs out the current user
def logout(request):
    #Sets the value to the cookie to an empty string
    #logging out the user
    response = HttpResponseRedirect('/')
    response.set_cookie("user","")
    return response

# Loads the page for a particular permalink
def permalink(request, url):
    
    
    
    username = util.checkLoggedIn(request)
    post = Post.objects.filter(link=url)
    
    if post:
        pages = Page.objects.all().order_by("id")
    
        return render_to_response("permalink.html", {"posts": post, "pages":pages, "username":username})

    else:
        #If post doesn't exist, show a 404 page
        raise Http404

#Creates a new post
def newpost(request):
    #Makes sure user is logged in, else redirect to home page
    username = util.checkLoggedIn(request)
    if not username:
        return HttpResponseRedirect('/')
    error = ""
    
    
    if request.method == "POST":
        
        
        form = blogForms.newPostForm(request.POST)
        #Check if there is an image
        if 'image' in request.FILES:
            image = request.FILES['image']
        else:
            image = None
        #saves post, returning an error if failed
        error, post = save(request, form, image, "Post")
        if not error:
            if not settings.DEBUG:
                tweet = post.title + " - " + "http://www.theconnectedwire.com/" + post.link
                twitter.updateTwitter(tweet)
                return HttpResponseRedirect('/' + "?tweet=" + tweet)
            else:
                return HttpResponseRedirect('/')
    
    else:
        form = blogForms.newPostForm()
    return render_to_response("newpost.html", {"form":form, "error": error, "username": username, "action":"newpost"}, context_instance = RequestContext(request))
    

def edit(request, url):
    #Makes sure user is logged in
    username = util.checkLoggedIn(request)
    if not username:
        return HttpResponseRedirect('/')
    error = ""
    if request.method == "POST":
        
        try:
            #Check if user clicked Delete Button
            if request.POST.has_key('Delete'):
                Post.objects.get(pk=url).delete()
                return HttpResponseRedirect('/')
            
            form = blogForms.newPostForm(request.POST)
            #Check if user uploaded image
            if 'image' in request.FILES:
                image = request.FILES['image']
            else:
                image = None
            #saves post, returning an error if failed
            error, post = save(request, form, image, "Post", url)
            
            if not error:
                return HttpResponseRedirect('/')
            else:
                return render_to_response("newpost.html", {"form":form, "post":url, "error":error, "username":username, "edit":True, "action":url}, context_instance = RequestContext(request))
        except ObjectDoesNotExist:
            raise Http404
    else:
        #Loads the post into the form, so it can be edited
        try:
            post = Post.objects.get(pk=url)
            url = str(url)
            if post:
                form = blogForms.newPostForm(initial = {'title':post.title, 'sourceUrl':post.sourceUrl, 'content':post.content})
                return render_to_response("newpost.html", {"form":form, "post":url, "error":error, "username":username, "edit":True, "action":url}, context_instance = RequestContext(request))
            else:
                raise Http404
        except ObjectDoesNotExist:
            raise Http404


def pageEdit(request, url):
    username = util.checkLoggedIn(request)
    if not username:
        return HttpResponseRedirect('/')
    error = ""
    if request.method == "POST":
        
        #Check if user clicked Delete Button
        if request.POST.has_key('Delete'):
            Page.objects.get(title=url).delete()
            return HttpResponseRedirect('/')
        
        form = blogForms.newPageForm(request.POST)
        #Check if user uploaded image
        if 'image' in request.FILES:
            image = request.FILES['image']
        else:
            image = None
        #saves page, returning an error if failed
        error = save(request, form, image, "Page", url)
        
        if not error:
            return HttpResponseRedirect('/')
        else:
            return render_to_response("newpage.html", {"form":form, "post":url, "error":error, "username":username, "edit":True, "action":url}, context_instance = RequestContext(request))
    
    else:
        #Loads the page into the form, so it can be edited
        try:
            page = Page.objects.get(title=url)
            url = str(url)
            if page:
                form = blogForms.newPageForm(initial = {'title':page.title, 'content':page.content})
                return render_to_response("newpage.html", {"form":form, "error":error, "username":username, "edit":True, "action":url}, context_instance = RequestContext(request))
            else:
                raise Http404
        except ObjectDoesNotExist:
            raise Http404

def page(request, page):
    username = util.checkLoggedIn(request)
    try:
        page = Page.objects.get(title=page)
    except ObjectDoesNotExist:
        raise Http404
    
    if page:
        pages = Page.objects.all().order_by("id")
        return render_to_response("page.html", {"page":page, "pages":pages, "username":username})
    else:
        raise Http404


def newpage(request):
    #Makes sure user is logged in, else redirect to home page
    username = util.checkLoggedIn(request)
    if not username:
        return HttpResponseRedirect('/')
    error = ""
    
    if request.method == "POST":
        
        
        form = blogForms.newPageForm(request.POST)
        #Check if there is an image
        if 'image' in request.FILES:
            image = request.FILES['image']
        else:
            image = None
        #saves post, returning an error if failed
        error = save(request, form, image, "Page")
        if not error:
            return HttpResponseRedirect('/')
    
    else:
        form = blogForms.newPageForm()
    return render_to_response("newpage.html", {"form":form, "error": error, "username": username, "action":"newpage"}, context_instance = RequestContext(request))


def search(request):
    pages = Page.objects.all()
    username = util.checkLoggedIn(request)
    return render_to_response("search.html", {"username": username, "pages": pages})

# Saves a post
def save(request, form, image, saveType, url = None):
        
        #Loads an instace of FileSystemStorage
        store = FileSystemStorage(paths.SITE_ROOT + '/images/')
        if image:
            #Checks if an image already exists
            #If it does, use that image as the url
            #Else save the image, and create a url
            if store.exists(image.name):
                imageURL = '/images/' + image.name
                featuredImage = imageURL
            else:
                storedImage = store.save(image.name, image)
                imageURL = "/images/" + storedImage
                featuredImage = imageURL
        else:
            imageURL = None
        
        
        if form.is_valid():
            if saveType == "Post":
                if url:
                    #If the post is being edited, delete the older version
                    published = Post.objects.get(pk=url).published
                    Post.objects.get(pk=url).delete()
                    posts = Categories.objects.filter(Post__id = url)
                    for i in posts:
                        i.delete()
                    featured = Featured.objects.filter(Post__id = url)
                    if featured:
                        featured.delete()
                else:
               
                    published = datetime.datetime.now()
                    
                month = published.month
                
                if month < 10:
                    newmonth = '0' + str(month)
                else:
                    newmonth = str(month)

                 #Create a post with the correct information
                
                
                title = request.POST['title']
                
                linkTitle = title.replace(' ', '-').lower()

                
                exclude = ['$', '#', '&', ';', ',']
                linkTitle = ''.join(ch for ch in linkTitle if ch not in exclude)
                
                link = str(published.year) + '/' + newmonth + '/' + linkTitle + '/'

                if not 'imageInPost' in request.POST:
                    imageURL = None
                else:
                    if not imageURL:
                        return "You didn't upload an image.", None
                
                post = Post(title = request.POST['title'],
                            sourceUrl = request.POST['sourceUrl'],
                            image = imageURL,
                            content = request.POST['content'],
                            published = published,
                            link = link)
                post.save()

                    

                if 'featured' in request.POST:
                    if not featuredImage:
                        return "You need an image", post
                    featured = Featured(Post = post, box = 1, imageURL = featuredImage)
                    featured.save()


                if 'categories' in request.POST:
                    categories = request.POST.getlist('categories')
                    for category in categories:
                        newCategory = Categories(Post = post, category = category)
                        newCategory.save()
                    return None, post
                else:
                    return "Something is amiss", post
            elif saveType == "Page":
                if url:
                    #If the post is being edited, delete the older version
                    Page.objects.get(title=url).delete()
                #Create a post with the correct information
                page = Page(title = request.POST['title'],
                            image = imageURL,
                            content = request.POST['content'])
                page.save()
                return None
        
        else:
            return "Something is amiss...", None
    
    