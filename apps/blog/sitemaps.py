from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.blog.models import Post
from apps.services.models import Plano


class StaticViewSitemap(Sitemap):
    """Sitemap para páginas estáticas"""
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['home', 'abrir_empresa', 'calculadora_clt_pj']

    def location(self, item):
        return reverse(item)


class BlogPostSitemap(Sitemap):
    """Sitemap para posts do blog"""
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.objects.filter(status='published').order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f'/blog/{obj.slug}/'


class ServicesSitemap(Sitemap):
    """Sitemap para página de serviços"""
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return ['/services/planos/']

    def location(self, item):
        return item


class PlanosSitemap(Sitemap):
    """Sitemap para planos ativos"""
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Plano.objects.filter(ativo=True)

    def lastmod(self, obj):
        return obj.created_at if hasattr(obj, 'created_at') else None

    def location(self, obj):
        return '/services/planos/'
