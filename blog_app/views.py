from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Comment


class PostListView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'obj'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'obj'
