from django.views.generic import ListView, View
from centr_osvita.blogs.models import Post


class PostsListView(ListView):
    model = Post
    template_name = 'blog/blogs.html'

    def get_queryset(self):
        object_list = Post.objects.all()
        return object_list
