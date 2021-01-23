from django import template
from django.db.models import Count
from ..models import Post, Comment

# from django.utils.safestring import mark_safe
# import markdown

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('./lastest_comments.html')
def show_latest_comments(count=5):
    latest_comments = Comment.objects.order_by('-created')[:count]
    return {'latest_comments': latest_comments}


# Most liked posts
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.objects.annotate(total_likes=Count('likes')).order_by('-total_likes')[:count]

# @register.filter(name='markdown')
# def markdown_format(text):
#     return mark_safe(markdown.markdown(text))
