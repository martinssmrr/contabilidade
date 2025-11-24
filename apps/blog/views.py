from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Post, Category


class PostListView(ListView):
    """View para listagem de posts do blog"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 8
    
    def get_queryset(self):
        """Retorna apenas posts publicados, excluindo os 3 mais recentes"""
        # Obter IDs dos 3 posts mais recentes
        recent_ids = list(Post.objects.filter(
            status='published'
        ).order_by('-created_at').values_list('id', flat=True)[:3])
        
        # Retornar posts excluindo os 3 mais recentes
        return Post.objects.filter(
            status='published'
        ).exclude(id__in=recent_ids).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """Adiciona dados extras ao contexto"""
        context = super().get_context_data(**kwargs)
        
        # Posts em destaque
        context['featured_posts'] = Post.objects.filter(
            status='published',
            is_featured=True
        ).order_by('-created_at')[:3]
        
        # Posts mais recentes (para a seção "Mais Recentes")
        recent_posts = Post.objects.filter(
            status='published'
        ).order_by('-created_at')[:3]
        
        context['latest_post'] = recent_posts[0] if recent_posts else None
        context['other_recent'] = recent_posts[1:3] if len(recent_posts) > 1 else []
        
        # Categorias
        context['categories'] = Category.objects.all()
        
        return context


class PostDetailView(DetailView):
    """View para detalhes de um post"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        """Retorna apenas posts publicados"""
        return Post.objects.filter(status='published')


def load_more_posts(request):
    """View AJAX para carregar mais posts"""
    page = int(request.GET.get('page', 2))
    per_page = 8
    
    # Obter IDs dos 3 posts mais recentes (excluir da listagem)
    recent_ids = list(Post.objects.filter(
        status='published'
    ).order_by('-created_at').values_list('id', flat=True)[:3])
    
    # Calcular offset
    offset = (page - 1) * per_page
    
    # Buscar posts
    posts = Post.objects.filter(
        status='published'
    ).exclude(id__in=recent_ids).order_by('-created_at')[offset:offset + per_page]
    
    # Verificar se há mais posts
    total_posts = Post.objects.filter(
        status='published'
    ).exclude(id__in=recent_ids).count()
    
    has_more = (offset + per_page) < total_posts
    
    # Renderizar HTML dos posts
    html = render_to_string('blog/partials/post_cards.html', {
        'posts': posts
    })
    
    return JsonResponse({
        'html': html,
        'has_more': has_more,
        'next_page': page + 1
    })

