from django import template
from django.db.models import Count
# from django.utils.safestring import mark_safe
# import markdown

register = template.Library()

from ..models import Post, Comment

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('./lastest_comments.html')
def show_latest_comments(count=5):
    latest_comments = Comment.objects.order_by('-created')[:count]
    return {'latest_comments': latest_comments}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.objects.annotate(total_comments=Count('comment')).order_by('-total_comments')[:count]

# @register.filter(name='markdown')
# def markdown_format(text):
#     return mark_safe(markdown.markdown(text))