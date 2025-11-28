from django import template

register = template.Library()


@register.inclusion_tag('partials/recent_posts.html')
def show_recent_posts(category_slug, count=3):
    """Retorna os últimos `count` posts publicados da categoria cujo slug é `category_slug`. Importa o modelo apenas na chamada para evitar problemas na descoberta das tags."""
    from apps.blog.models import Post

    posts = Post.objects.filter(status='published', category__slug=category_slug).order_by('-created_at')[:count]
    return {'recent_posts': posts}
