from django.contrib import admin
from django.db import models
from django.forms import Textarea
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'slug', 'author', 'status')
        }),
        ('Conteúdo', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    # Editor WYSIWYG usando TinyMCE via CDN
    class Media:
        js = (
            'https://cdn.tiny.cloud/1/no-api-key/tinymce/6/tinymce.min.js',
            'js/tinymce-config.js',
        )
    
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={
                'class': 'tinymce',
                'rows': 20,
                'cols': 80
            })
        },
    }
    
    def save_model(self, request, obj, form, change):
        """Define o autor como o usuário atual se não definido"""
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

