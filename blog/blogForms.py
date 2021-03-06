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

from django import forms
import models

class SignupForm(forms.Form):
    username = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput, max_length = 10)
    verify = forms.CharField(widget=forms.PasswordInput, max_length = 10)
    auth = forms.CharField(max_length = 20)
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length = 10)
    password = forms.CharField(widget=forms.PasswordInput, max_length = 10)
    
class newPostForm(forms.Form):
    title = forms.CharField(max_length = 100)
    sourceUrl = forms.CharField(max_length = 100, required = False)
    image = forms.ImageField(required = False)
    content = forms.CharField(widget=forms.Textarea)
    categories = forms.MultipleChoiceField(choices = models.CATEGORIES, widget = forms.CheckboxSelectMultiple)
    featured = forms.BooleanField(required = False)
    imageInPost = forms.BooleanField(required = False)

class newPageForm(forms.Form):
    title = forms.CharField(max_length = 100)
    image = forms.ImageField(required = False)
    content = forms.CharField(widget=forms.Textarea)

class newEpisodeForm(forms.Form):
    title = forms.CharField(max_length = 100)
    episode = forms.CharField(max_length = 100)
    image = forms.ImageField()
    showNotes = forms.CharField(widget=forms.Textarea)
    size = forms.CharField(max_length = 100)
    duration = forms.CharField(max_length = 100)