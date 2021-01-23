from django.urls import path
from . import views

app_name = 'blog_app'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
        views.PostDetailView.as_view(),
        name='post_detail'),
    path('add_post', views.PostCreateView.as_view(), name='post_add'),
    path('blogpost-like/<int:pk>', views.blog_post_like, name="blogpost_like"),


]
