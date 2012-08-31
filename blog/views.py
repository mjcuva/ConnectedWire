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

#Allows the page to be rendered
from django.shortcuts import render_to_response

# Allows redirects, as well as 404 pages
from django.http import HttpResponseRedirect, Http404

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

#PIL Image Library
from PIL import Image

#Time Function
import datetime

import twitter

import string

import re

import stats

import paths

from django.conf import settings

# Mobile user agents
reg_b = re.compile(r"android.+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|meego.+mobile|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino", re.I|re.M)
reg_v = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\\-|your|zeto|zte\\-", re.I|re.M)

# Checks if user is mobile
def checkMobile(request):
    request.mobile = False
    # If there is a user agent
    if request.META.has_key('HTTP_USER_AGENT'):
        #Checks the user agent agianst list of agents
        user_agent = request.META['HTTP_USER_AGENT']
        b = reg_b.search(user_agent)
        v = reg_v.search(user_agent[0:4])
        if b or v:
            return True
        else:
            return False






# Homepage
def index(request):
    
    isMobile = checkMobile(request)
    
    # Checks if a user is logged in
    username = util.checkLoggedIn(request)
    
    # Queries the database
    posts = Post.objects.all().order_by("-published")
    
    # Gets the templates
    template = "base.html"
    mobileTemplate = "mobile/base.html"
    page_template = "index.html"
    mobilePage_template = "mobile/index.html"
    
    # If the request is coming from an ajax request
    # and sets the template accordingly
    if request.is_ajax():
        template = page_template
        mobileTemplate = mobilePage_template
    
    # Gets the total wordcount
    count = stats.getWordCount()

    # Get featured posts
    featured = []
    cats = []
    for i in range(1,5):
        try:
            featured.append(Featured.objects.filter(box = i).order_by('-id')[0])
            feature = Featured.objects.filter(box = i).order_by('-id')[0]
            categories = Categories.objects.filter(Post__title=feature.Post.title)
            for i in categories:
                if not str(i) == 'News':
                    cats.append(i)
                    added = True
            if not added:
                cats.append('News')
            added = False

        except IndexError:
            pass

    
    
    # Gets all of the pages
    pages = Page.objects.all().order_by("id")
    
    # Renders the page
    
    if not isMobile:
        return render_to_response(template, {"posts" : posts, "pages":pages, "username": username, "wordcount": count, "featured": featured, "cats":cats}, context_instance=RequestContext(request))
    else:
        return render_to_response(mobileTemplate, {"posts": posts}, context_instance=RequestContext(request))

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
    
    isMobile = checkMobile(request)

    
    username = util.checkLoggedIn(request)
    
    template = "base.html"
    mobileTemplate = "mobile/base.html"
    page_template = "index.html"
    mobilePage_template = "mobile/index.html"
    
    if request.is_ajax():
        template = page_template
        mobileTemplate = mobilePage_template
    
    posts = []
    catList = Categories.objects.filter(category=category).order_by('-id')
    
    for i in catList:
        posts.append(i.Post)
    
    pages = Page.objects.all().order_by("id")
    

    
    if not isMobile:
        return render_to_response(template, {"posts" : posts, "pages":pages, "username": username}, context_instance=RequestContext(request))
    else:
        return render_to_response(mobileTemplate, {"posts": posts}, context_instance=RequestContext(request))

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
                    response = HttpResponseRedirect('/')
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
    return render_to_response("login.html", {"form": form, "error": error}, context_instance=RequestContext(request))

#Logs out the current user
def logout(request):
    #Sets the value to the cookie to an empty string
    #logging out the user
    response = HttpResponseRedirect('/')
    response.set_cookie("user","")
    return response

# Loads the page for a particular permalink
def permalink(request, url):
    
    isMobile = checkMobile(request)
    
    username = util.checkLoggedIn(request)
    post = Post.objects.filter(link=url)
    
    if post:
        pages = Page.objects.all().order_by("id")
        if not isMobile:
            return render_to_response("permalink.html", {"posts": post, "pages":pages, "username":username})
        else:
            return render_to_response("mobile/permalink.html", {"posts":post})
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
        error, post = save(request,  form, image, "Post")
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
            else:
                storedImage = store.save(image.name, image)
                imageURL = "/images/" + storedImage
        else:
            imageURL = None
        
        
        if form.is_valid():
            if saveType == "Post":
                if url:
                    #If the post is being edited, delete the older version
                    Post.objects.get(pk=url).delete()
                    posts = Categories.objects.filter(Post__id = url)
                    for i in posts:
                        i.delete()
                    featured = Featured.objects.filter(Post__id = url)
                    if featured:
                        featured.delete()

                #Create a post with the correct information
                
                published = datetime.datetime.now()
                
                month = published.month
                
                if month < 10:
                    newmonth = '0' + str(month)
                else:
                    newmonth = str(month)
                
                title = request.POST['title']
                
                linkTitle = title.replace(' ', '-').lower()

                
                exclude = ['$', '#', '&', ';', ',']
                linkTitle = ''.join(ch for ch in linkTitle if ch not in exclude)
                
                link = str(published.year) + '/' + newmonth + '/' + linkTitle + '/'
                
                post = Post(title = request.POST['title'],
                            sourceUrl = request.POST['sourceUrl'],
                            image = imageURL,
                            content = request.POST['content'],
                            published = published,
                            link = link)
                post.save()

                    
                featuredBox = request.POST['box']

                if featuredBox != str(0):
                    if not imageURL:
                        return "You need an image", post
                    featured = Featured(Post = post, box = featuredBox, imageURL = imageURL)
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
    
    