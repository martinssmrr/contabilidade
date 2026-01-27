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
            'contabilidade_mei',
            'endereco_virtual',
            'certificado_digital',
            'emissor_nota_fiscal',
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
