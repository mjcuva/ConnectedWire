from django import template
from django.template.defaultfilters import stringfilter
from blog.models import Categories, Post

register = template.Library()

@register.filter
@stringfilter
def getCat(title):
	return Categories.objects.filter(Post__title=title)
