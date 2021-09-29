
from django import template
from ..models import Vote
register = template.Library()

@register.simple_tag
def votesfor(candidate, category):
    result = Vote.objects.filter(candidate=candidate, category=category).count()
    return result