from django.contrib import admin
from .models import SocialMedia

# Register your models here.

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active', 'platform']
    search_fields = ['platform', 'url']
    ordering = ['order', 'platform']
