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

class newPageForm(forms.Form):
	title = forms.CharField(max_length = 100)
	image = forms.ImageField(required = False)
	content = forms.CharField(widget=forms.Textarea)