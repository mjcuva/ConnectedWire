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