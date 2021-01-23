from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Comment
from user_app.models import Profile


class PostListView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'obj'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.filter(slug=self.kwargs['slug']).first()
        context["comments_list"] = Comment.objects.filter(post=post)
        return context
    

class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = ['title', 'body', 'img']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


# to_page=0 - homepage to_page=1 - detailview
def blog_post_like(request, to_page):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = post.likes.filter(id=request.user.id).first()
    if is_liked:
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    if to_page == 0:
        return HttpResponseRedirect(reverse('blog_app:post_list'))
    else:
        return HttpResponseRedirect(reverse('blog_app:post_detail',
                                            kwargs={"year": post.created.year, "month": post.created.month,
                                                    "day": post.created.day, "slug": post.slug}))




