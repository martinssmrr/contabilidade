from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.blog.models import Post


class StaticViewSitemap(Sitemap):
    """Sitemap para páginas estáticas"""
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return [
            'home',
            'abrir_empresa',
            'deixar_mei',
            'trocar_contador',
            'contabilidade_completa',
            'assessoria',
            'calculadora_clt_pj',
            'sobre',
            'termos_de_uso',
            'politica_de_privacidade',
        ]

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
        return ['/services/', '/services/planos/']

    def location(self, item):
        return item


class ImagesSitemap(Sitemap):
    """Sitemap para imagens principais (logo, etc)"""
    changefreq = 'yearly'
    priority = 0.5

    def items(self):
        return [
            '/static/img/logo.webp',
            '/static/img/logo.png',
        ]

    def location(self, item):
        return item
