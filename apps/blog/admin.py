from django.contrib import admin
from django.db import models
from django.forms import Textarea
from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_featured', 'status', 'focus_keyword', 'created_at', 'updated_at')
    list_filter = ('status', 'is_featured', 'category', 'created_at', 'author')
    search_fields = ('title', 'content', 'meta_title', 'meta_description', 'focus_keyword')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_editable = ('is_featured', 'status')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'slug', 'category', 'author', 'status', 'is_featured')
        }),
        ('Conteúdo', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('SEO - Otimização para Buscadores', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'focus_keyword', 'canonical_url'),
            'description': 'Campos opcionais para otimização SEO. Se vazios, serão gerados automaticamente.',
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        """Define o autor como o usuário atual se não definido"""
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

