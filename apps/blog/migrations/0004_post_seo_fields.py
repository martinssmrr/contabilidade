from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='meta_title',
            field=models.CharField(
                blank=True,
                help_text='Título para SEO (máx. 70 caracteres). Se vazio, usa o título do post.',
                max_length=70,
                verbose_name='Meta Title (SEO)',
            ),
        ),
        migrations.AddField(
            model_name='post',
            name='meta_description',
            field=models.CharField(
                blank=True,
                help_text='Descrição para SEO (máx. 160 caracteres). Se vazio, usa o resumo do post.',
                max_length=160,
                verbose_name='Meta Description (SEO)',
            ),
        ),
        migrations.AddField(
            model_name='post',
            name='meta_keywords',
            field=models.CharField(
                blank=True,
                help_text='Palavras-chave separadas por vírgula. Ex: contabilidade, MEI, impostos',
                max_length=255,
                verbose_name='Meta Keywords (SEO)',
            ),
        ),
        migrations.AddField(
            model_name='post',
            name='focus_keyword',
            field=models.CharField(
                blank=True,
                help_text='Palavra-chave principal para otimização SEO do post.',
                max_length=100,
                verbose_name='Palavra-chave Principal (SEO)',
            ),
        ),
        migrations.AddField(
            model_name='post',
            name='canonical_url',
            field=models.URLField(
                blank=True,
                help_text='URL canônica personalizada. Se vazio, usa a URL padrão do post.',
                max_length=500,
                verbose_name='URL Canônica (SEO)',
            ),
        ),
    ]
