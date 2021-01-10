from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Comment


class PostListView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'obj'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'obj'


class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = ['title', 'body', 'img']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)