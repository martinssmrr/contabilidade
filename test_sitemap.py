#!/usr/bin/env python
"""Script para testar o sitemap localmente"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao360_project.settings')
django.setup()

from django.urls import reverse
from apps.blog.sitemaps import StaticViewSitemap, BlogPostSitemap, ServicesSitemap, ImagesSitemap

print("=== Testando StaticViewSitemap ===")
sitemap = StaticViewSitemap()
for item in sitemap.items():
    try:
        url = reverse(item)
        print(f"✓ {item}: {url}")
    except Exception as e:
        print(f"✗ {item}: ERRO - {e}")

print("\n=== Testando BlogPostSitemap ===")
blog_sitemap = BlogPostSitemap()
posts = blog_sitemap.items()
print(f"Total de posts publicados: {len(posts)}")
for post in posts[:3]:  # Mostra apenas os 3 primeiros
    print(f"  - {post.title}: /blog/{post.slug}/")

print("\n=== Testando ServicesSitemap ===")
services_sitemap = ServicesSitemap()
for item in services_sitemap.items():
    print(f"✓ {item}")

print("\n=== Testando ImagesSitemap ===")
images_sitemap = ImagesSitemap()
for item in images_sitemap.items():
    print(f"✓ {item}")

print("\n=== Teste concluído ===")
