from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
try:
    from django_ckeditor_5.fields import CKEditor5Field
except ImportError:
    # Fallback se não estiver instalado
    class CKEditor5Field(models.TextField):
        def __init__(self, *args, **kwargs):
            # Remove custom arguments not supported by TextField
            kwargs.pop('config_name', None)
            super().__init__(*args, **kwargs)

User = get_user_model()


class Category(models.Model):
    """Modelo para categorias do blog"""
    
    name = models.CharField('Nome', max_length=100, unique=True)
    slug = models.SlugField('Slug', max_length=100, unique=True, blank=True)
    description = models.TextField('Descrição', blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Gera slug automaticamente se não fornecido"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Retorna a URL da categoria"""
        return reverse('blog:category', kwargs={'slug': self.slug})


class Post(models.Model):
    """Modelo para posts do blog"""
    
    STATUS_CHOICES = (
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
    )
    
    title = models.CharField('Título', max_length=200)
    slug = models.SlugField('Slug', max_length=200, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Categoria'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='blog_posts',
        verbose_name='Autor'
    )
    content = CKEditor5Field('Conteúdo', config_name='extends')
    excerpt = models.TextField('Resumo', max_length=300, blank=True, help_text='Breve descrição do post (máx. 300 caracteres)')
    featured_image = models.ImageField(
        'Imagem de Destaque', 
        upload_to='blog/images/%Y/%m/',
        blank=True,
        null=True
    )
    is_featured = models.BooleanField('Em Destaque', default=False, help_text='Marque para exibir na seção de destaques')
    status = models.CharField(
        'Status',
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Gera slug automaticamente se não fornecido"""
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        
        # Gera excerpt automaticamente se não fornecido
        if not self.excerpt and self.content:
            # Remove tags HTML e pega os primeiros 300 caracteres
            import re
            clean_content = re.sub('<[^<]+?>', '', self.content)
            self.excerpt = clean_content[:300] + '...' if len(clean_content) > 300 else clean_content
            
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Retorna a URL do post"""
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

