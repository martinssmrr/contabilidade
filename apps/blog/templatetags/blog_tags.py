from django import template
import re

register = template.Library()


@register.filter(name='reading_time')
def reading_time(content):
    """Calcula o tempo estimado de leitura de um conteúdo HTML"""
    if not content:
        return 1
    clean_content = re.sub('<[^<]+?>', '', str(content))
    word_count = len(clean_content.split())
    minutes = max(1, round(word_count / 200))
    return minutes


@register.filter(name='strip_html')
def strip_html(value):
    """Remove todas as tags HTML de um texto"""
    if not value:
        return ''
    return re.sub('<[^<]+?>', '', str(value))


# Mapeamento de slugs de página para categorias e títulos
CATEGORY_MAPPING = {
    'abrir-empresa': {
        'category_slug': 'abrir-empresa',
        'title': 'Abrir Empresa'
    },
    'deixar-mei': {
        'category_slug': 'deixar-mei',
        'title': 'Deixar o MEI'
    },
    'trocar-contador': {
        'category_slug': 'trocar-contador',
        'title': 'Trocar de Contador'
    },
    'contabilidade-completa': {
        'category_slug': 'contabilidade-completa',
        'title': 'Contabilidade Completa'
    },
    'assessoria': {
        'category_slug': 'assessoria-contabil',
        'title': 'Assessoria Contábil'
    },
}


@register.inclusion_tag('partials/recent_posts.html')
def show_recent_posts(page_slug, count=3):
    """
    Retorna os últimos `count` posts publicados da categoria correspondente ao slug da página.
    
    Mapeamento:
    - abrir-empresa → categoria 'abrir-empresa'
    - deixar-mei → categoria 'deixar-mei'
    - trocar-contador → categoria 'trocar-contador'
    - contabilidade-completa → categoria 'contabilidade-completa'
    - assessoria → categoria 'assessoria-contabil'
    """
    from apps.blog.models import Post
    
    # Buscar mapeamento ou usar o slug diretamente como fallback
    mapping = CATEGORY_MAPPING.get(page_slug, {
        'category_slug': page_slug,
        'title': page_slug.replace('-', ' ').title()
    })
    
    category_slug = mapping['category_slug']
    category_title = mapping['title']
    
    posts = Post.objects.filter(
        status='published', 
        category__slug=category_slug
    ).order_by('-created_at')[:count]
    
    return {
        'recent_posts': posts,
        'category_title': category_title,
        'has_posts': posts.exists()
    }
