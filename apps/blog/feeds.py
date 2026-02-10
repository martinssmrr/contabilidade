from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse
from .models import Post


class BlogPostsFeed(Feed):
    """RSS Feed para posts do blog da Vetorial Contabilidade"""
    
    title = "Blog Vetorial Contabilidade"
    description = "Artigos sobre contabilidade, abertura de empresa, MEI, impostos e gestão empresarial."
    link = "/blog/"
    
    def items(self):
        return Post.objects.filter(status='published').order_by('-created_at')[:20]
    
    def item_title(self, item):
        return item.seo_title
    
    def item_description(self, item):
        return truncatewords_html(item.content, 50)
    
    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_pubdate(self, item):
        return item.created_at
    
    def item_updateddate(self, item):
        return item.updated_at
    
    def item_author_name(self, item):
        return item.author.get_full_name() or 'Vetorial Contabilidade'
    
    def item_categories(self, item):
        cats = []
        if item.category:
            cats.append(item.category.name)
        if item.focus_keyword:
            cats.append(item.focus_keyword)
        return cats


class CategoryFeed(Feed):
    """RSS Feed por categoria do blog"""
    
    def get_object(self, request, slug):
        from .models import Category
        return Category.objects.get(slug=slug)
    
    def title(self, obj):
        return f"Vetorial Contabilidade - {obj.name}"
    
    def description(self, obj):
        return obj.description or f"Artigos sobre {obj.name} no blog da Vetorial Contabilidade."
    
    def link(self, obj):
        return "/blog/"
    
    def items(self, obj):
        return Post.objects.filter(
            status='published',
            category=obj
        ).order_by('-created_at')[:20]
    
    def item_title(self, item):
        return item.seo_title
    
    def item_description(self, item):
        return truncatewords_html(item.content, 50)
    
    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_pubdate(self, item):
        return item.created_at
