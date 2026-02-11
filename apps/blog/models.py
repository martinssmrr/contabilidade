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


class Tag(models.Model):
    """Modelo para tags do blog"""
    
    name = models.CharField('Nome', max_length=50, unique=True)
    slug = models.SlugField('Slug', max_length=50, unique=True, blank=True)
    
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug': self.slug})


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
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts',
        verbose_name='Tags'
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
    
    # SEO Fields
    meta_title = models.CharField(
        'Meta Title (SEO)',
        max_length=70,
        blank=True,
        help_text='Título para SEO (máx. 70 caracteres). Se vazio, usa o título do post.'
    )
    meta_description = models.CharField(
        'Meta Description (SEO)',
        max_length=160,
        blank=True,
        help_text='Descrição para SEO (máx. 160 caracteres). Se vazio, usa o resumo do post.'
    )
    meta_keywords = models.CharField(
        'Meta Keywords (SEO)',
        max_length=255,
        blank=True,
        help_text='Palavras-chave separadas por vírgula. Ex: contabilidade, MEI, impostos'
    )
    focus_keyword = models.CharField(
        'Palavra-chave Principal (SEO)',
        max_length=100,
        blank=True,
        help_text='Palavra-chave principal para otimização SEO do post.'
    )
    canonical_url = models.URLField(
        'URL Canônica (SEO)',
        max_length=500,
        blank=True,
        help_text='URL canônica personalizada. Se vazio, usa a URL padrão do post.'
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
    
    @property
    def seo_title(self):
        """Retorna o meta_title se definido, senão o título do post"""
        return self.meta_title if self.meta_title else self.title
    
    @property
    def seo_description(self):
        """Retorna meta_description se definido, senão o excerpt"""
        if self.meta_description:
            return self.meta_description
        if self.excerpt:
            return self.excerpt[:160]
        if self.content:
            import re
            clean = re.sub('<[^<]+?>', '', self.content)
            return clean[:160]
        return ''
    
    @property
    def seo_keywords(self):
        """Retorna meta_keywords ou gera a partir da categoria"""
        if self.meta_keywords:
            return self.meta_keywords
        keywords = ['contabilidade', 'vetorial contabilidade']
        if self.category:
            keywords.append(self.category.name.lower())
        if self.focus_keyword:
            keywords.insert(0, self.focus_keyword.lower())
        return ', '.join(keywords)
    
    @property
    def reading_time(self):
        """Calcula o tempo estimado de leitura em minutos"""
        import re
        if not self.content:
            return 1
        clean_content = re.sub('<[^<]+?>', '', self.content)
        word_count = len(clean_content.split())
        minutes = max(1, round(word_count / 200))
        return minutes

