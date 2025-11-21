from django.db import models

# Create your models here.

class SocialMedia(models.Model):
    """
    Model para gerenciar links de redes sociais exibidos no footer.
    """
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter / X'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('whatsapp', 'WhatsApp'),
    ]
    
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, verbose_name='Plataforma', unique=True)
    url = models.URLField(max_length=500, verbose_name='URL/Link')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    order = models.IntegerField(default=0, verbose_name='Ordem de Exibição')
    
    class Meta:
        verbose_name = 'Rede Social'
        verbose_name_plural = 'Redes Sociais'
        ordering = ['order', 'platform']
    
    def __str__(self):
        return f"{self.get_platform_display()}"

