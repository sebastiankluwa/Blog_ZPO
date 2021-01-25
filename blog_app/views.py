from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from .models import Post, Comment
from .forms import CommentCreateForm
from user_app.models import Profile


class PostListView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'obj'


class PostDetailView(DetailView, FormMixin):
    model = Post
    template_name = 'post.html'
    context_object_name = 'obj'
    form_class = CommentCreateForm

    def get_success_url(self):
        return reverse('blog_app:post_detail', kwargs={'year': self.object.publish.year,
                                                'month': self.object.publish.month,
                                                'day': self.object.publish.day,
                                                'slug': self.object.slug})
#      path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
#         views.PostDetailView.as_view(),
#         name='post_detail')

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post = Post.objects.filter(slug=self.kwargs['slug']).first()
        context["comments_list"] = Comment.objects.filter(post=post)
        if self.request.user.is_authenticated:
            context['form'] = CommentCreateForm(initial={'post': self.object, 'author': self.request.user.profile})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        form.save()
        return super(PostDetailView, self).form_valid(form)
    

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

    post.num_of_popularity()
    if to_page == 0:
        return HttpResponseRedirect(reverse('blog_app:post_list'))
    else:
        return HttpResponseRedirect(reverse('blog_app:post_detail',
                                            kwargs={"year": post.created.year, "month": post.created.month,
                                                    "day": post.created.day, "slug": post.slug}))


# def comment_create(request):
#     if request.method == "POST":
#         c_form = CommentCreateForm(data=request.POST)
#         if c_form.is_valid():
#             instance = c_form.save(commit=False)
#             instance.author = request.user.profile
#             instance.save()
#     else:
#         c_form = CommentCreateForm()
#     context = {
#         'c_form': c_form,
#     }

#     return render(request, context)


