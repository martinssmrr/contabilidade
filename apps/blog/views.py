from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class PostListView(ListView):
    """View para listagem de posts do blog"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        """Retorna apenas posts publicados"""
        return Post.objects.filter(status='published').order_by('-created_at')


class PostDetailView(DetailView):
    """View para detalhes de um post"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        """Retorna apenas posts publicados"""
        return Post.objects.filter(status='published')

