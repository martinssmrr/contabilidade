from django.contrib import admin
from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'position', 'content']
    list_editable = ['is_active', 'order']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Informações Principais', {
            'fields': ('name', 'position', 'photo', 'content')
        }),
        ('Configurações', {
            'fields': ('is_active', 'order', 'created_at')
        }),
    )
