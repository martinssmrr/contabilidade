from django.db import models
from django.utils import timezone


class Testimonial(models.Model):
    """Modelo para depoimentos de clientes"""
    name = models.CharField('Nome', max_length=100)
    position = models.CharField('Cargo/Empresa', max_length=150)
    photo = models.ImageField('Foto', upload_to='testimonials/', blank=True, null=True)
    content = models.TextField('Depoimento')
    is_active = models.BooleanField('Ativo', default=True)
    order = models.IntegerField('Ordem', default=0, help_text='Ordem de exibição (menor aparece primeiro)')
    created_at = models.DateTimeField('Criado em', default=timezone.now)
    
    class Meta:
        verbose_name = 'Depoimento'
        verbose_name_plural = 'Depoimentos'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.position}"
