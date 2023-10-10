from django.views.generic import ListView, DetailView
from centr_osvita.blogs.models import Post


class PostsListView(ListView):
    model = Post
    template_name = 'blog/blogs.html'
    queryset = Post.objects.all()


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/blog.html'
    queryset = Post.objects.all()
