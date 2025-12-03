from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from .models import Document, NotaFiscal, DocumentoEmpresa, ExtratoBancario, DocumentoCliente

# Register your models here.

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'categoria', 'visivel_para_cliente', 'tamanho_arquivo', 'criado_em']
    list_filter = ['categoria', 'visivel_para_cliente', 'criado_em']
    search_fields = ['titulo', 'descricao', 'usuario__username']
    raw_id_fields = ['usuario']
    readonly_fields = ['criado_em', 'atualizado_em', 'tamanho_arquivo', 'extensao_arquivo']


@admin.register(NotaFiscal)
class NotaFiscalAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente_info', 'nome_arquivo_display', 'data_upload', 'enviado_por', 'tamanho_arquivo']
    list_filter = ['data_upload', 'enviado_por']
    search_fields = ['cliente__username', 'cliente__email', 'cliente__first_name', 'cliente__last_name']
    raw_id_fields = ['cliente', 'enviado_por']
    readonly_fields = ['data_upload', 'tamanho_arquivo', 'nome_arquivo']
    date_hierarchy = 'data_upload'
    
    fieldsets = (
        ('Informações do Cliente', {
            'fields': ('cliente',)
        }),
        ('Arquivo', {
            'fields': ('arquivo_pdf', 'nome_arquivo', 'tamanho_arquivo')
        }),
        ('Controle', {
            'fields': ('enviado_por', 'data_upload', 'observacoes')
        }),
    )
    
    def cliente_info(self, obj):
        """Exibe informações do cliente de forma mais clara."""
        nome = obj.cliente.get_full_name() or obj.cliente.username
        return format_html('<strong>{}</strong><br><small>{}</small>', nome, obj.cliente.email)
    cliente_info.short_description = 'Cliente'
    
    def nome_arquivo_display(self, obj):
        """Exibe o nome do arquivo com ícone."""
        return format_html('<i class="fas fa-file-pdf" style="color: red;"></i> {}', obj.nome_arquivo)
    nome_arquivo_display.short_description = 'Arquivo'
    
    def get_queryset(self, request):
        """Otimiza consultas incluindo relacionamentos."""
        qs = super().get_queryset(request)
        return qs.select_related('cliente', 'enviado_por')
    
    def save_model(self, request, obj, form, change):
        """Preenche automaticamente o campo enviado_por se não estiver definido."""
        if not obj.enviado_por:
            obj.enviado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(DocumentoEmpresa)
class DocumentoEmpresaAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'cliente_info', 'categoria', 'nome_arquivo_display', 'data_upload', 'enviado_por']
    list_filter = ['categoria', 'data_upload', 'enviado_por']
    search_fields = ['titulo', 'descricao', 'cliente__username', 'cliente__email', 'cliente__first_name', 'cliente__last_name']
    raw_id_fields = ['cliente', 'enviado_por']
    readonly_fields = ['data_upload', 'tamanho_arquivo', 'nome_arquivo', 'extensao_arquivo']
    date_hierarchy = 'data_upload'
    
    fieldsets = (
        ('Informações do Cliente', {
            'fields': ('cliente',)
        }),
        ('Dados do Documento', {
            'fields': ('titulo', 'categoria', 'descricao')
        }),
        ('Arquivo', {
            'fields': ('arquivo', 'nome_arquivo', 'extensao_arquivo', 'tamanho_arquivo')
        }),
        ('Controle', {
            'fields': ('enviado_por', 'data_upload')
        }),
    )
    
    def cliente_info(self, obj):
        """Exibe informações do cliente de forma mais clara."""
        nome = obj.cliente.get_full_name() or obj.cliente.username
        return format_html('<strong>{}</strong><br><small>{}</small>', nome, obj.cliente.email)
    cliente_info.short_description = 'Cliente'
    
    def nome_arquivo_display(self, obj):
        """Exibe o nome do arquivo com ícone baseado na extensão."""
        extensao = obj.extensao_arquivo
        icon_class = 'fa-file'
        
        if extensao in ['pdf']:
            icon_class = 'fa-file-pdf'
        elif extensao in ['doc', 'docx']:
            icon_class = 'fa-file-word'
        elif extensao in ['xls', 'xlsx']:
            icon_class = 'fa-file-excel'
        elif extensao in ['jpg', 'jpeg', 'png', 'gif']:
            icon_class = 'fa-file-image'
        elif extensao in ['zip', 'rar', '7z']:
            icon_class = 'fa-file-archive'
        
        return format_html('<i class="fas {}" style="color: #007bff;"></i> {}', icon_class, obj.nome_arquivo)
    nome_arquivo_display.short_description = 'Arquivo'
    
    def get_queryset(self, request):
        """Otimiza consultas incluindo relacionamentos."""
        qs = super().get_queryset(request)
        return qs.select_related('cliente', 'enviado_por')
    
    def save_model(self, request, obj, form, change):
        """Preenche automaticamente o campo enviado_por se não estiver definido."""
        if not obj.enviado_por:
            obj.enviado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(ExtratoBancario)
class ExtratoBancarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente_info', 'mes_ano', 'nome_arquivo_display', 'data_upload', 'tamanho_arquivo']
    list_filter = ['mes_ano', 'data_upload', 'cliente']
    search_fields = ['cliente__username', 'cliente__email', 'cliente__first_name', 'cliente__last_name', 'mes_ano', 'observacoes']
    raw_id_fields = ['cliente']
    readonly_fields = ['data_upload', 'tamanho_arquivo', 'nome_arquivo', 'extensao_arquivo']
    date_hierarchy = 'data_upload'
    
    fieldsets = (
        ('Informações do Cliente', {
            'fields': ('cliente',)
        }),
        ('Dados do Extrato', {
            'fields': ('mes_ano', 'observacoes')
        }),
        ('Arquivo', {
            'fields': ('arquivo', 'nome_arquivo', 'tamanho_arquivo', 'extensao_arquivo')
        }),
        ('Controle', {
            'fields': ('data_upload',)
        }),
    )
    
    def cliente_info(self, obj):
        """Exibe informações do cliente de forma mais clara."""
        nome = obj.cliente.get_full_name() or obj.cliente.username
        return format_html('<strong>{}</strong><br><small>{}</small>', nome, obj.cliente.email)
    cliente_info.short_description = 'Cliente'
    
    def nome_arquivo_display(self, obj):
        """Exibe o nome do arquivo com ícone."""
        extensao = obj.extensao_arquivo or 'file'
        icon_class = 'fa-file'
        
        if extensao in ['pdf']:
            icon_class = 'fa-file-pdf'
        elif extensao in ['jpg', 'jpeg', 'png', 'gif']:
            icon_class = 'fa-file-image'
        elif extensao in ['xls', 'xlsx', 'csv']:
            icon_class = 'fa-file-excel'
        elif extensao in ['zip', 'rar', '7z']:
            icon_class = 'fa-file-archive'
        
        return format_html('<i class="fas {}" style="color: #28a745;"></i> {}', icon_class, obj.nome_arquivo)
    nome_arquivo_display.short_description = 'Arquivo'
    
    def get_queryset(self, request):
        """Otimiza consultas incluindo relacionamentos."""
        qs = super().get_queryset(request)
        return qs.select_related('cliente')


@admin.register(DocumentoCliente)
class DocumentoClienteAdmin(admin.ModelAdmin):
    """
    Admin customizado para DocumentoCliente com notificação automática por e-mail.
    
    Features:
    - Upload organizado de documentos
    - Preenche automaticamente o campo enviado_por
    - Exibe status de visualização e notificação
    - Interface profissional com ícones
    - Busca avançada
    """
    
    list_display = [
        'id',
        'titulo_display',
        'cliente_info',
        'tipo_documento',
        'nome_arquivo_display',
        'status_notificacao',
        'status_visualizacao',
        'data_envio',
        'enviado_por'
    ]
    
    list_filter = [
        'tipo_documento',
        'notificacao_enviada',
        'visualizado',
        'data_envio',
        'enviado_por'
    ]
    
    search_fields = [
        'titulo',
        'descricao',
        'cliente__username',
        'cliente__email',
        'cliente__first_name',
        'cliente__last_name'
    ]
    
    raw_id_fields = ['cliente', 'enviado_por']
    
    readonly_fields = [
        'data_envio',
        'tamanho_arquivo',
        'nome_arquivo',
        'extensao_arquivo',
        'notificacao_enviada',
        'data_notificacao',
        'visualizado',
        'data_visualizacao',
        'dias_desde_envio'
    ]
    
    date_hierarchy = 'data_envio'
    
    fieldsets = (
        ('🎯 Destinatário', {
            'fields': ('cliente',),
            'description': 'Selecione o cliente que receberá este documento'
        }),
        ('📄 Dados do Documento', {
            'fields': ('tipo_documento', 'titulo', 'descricao', 'arquivo'),
            'description': 'Preencha as informações do documento'
        }),
        ('📁 Informações do Arquivo', {
            'fields': ('nome_arquivo', 'extensao_arquivo', 'tamanho_arquivo'),
            'classes': ('collapse',),
        }),
        ('✉️ Status da Notificação', {
            'fields': ('notificacao_enviada', 'data_notificacao'),
            'classes': ('collapse',),
            'description': 'Status do envio do e-mail automático'
        }),
        ('👁️ Visualização pelo Cliente', {
            'fields': ('visualizado', 'data_visualizacao'),
            'classes': ('collapse',),
        }),
        ('⚙️ Controle', {
            'fields': ('enviado_por', 'data_envio', 'dias_desde_envio'),
            'classes': ('collapse',),
        }),
    )
    
    def titulo_display(self, obj):
        """Exibe o título com ícone."""
        return format_html('📄 <strong>{}</strong>', obj.titulo)
    titulo_display.short_description = 'Título'
    
    def cliente_info(self, obj):
        """Exibe informações do cliente de forma clara."""
        nome = obj.cliente.get_full_name() or obj.cliente.username
        return format_html('<strong>{}</strong><br><small>{}</small>', nome, obj.cliente.email)
    cliente_info.short_description = 'Cliente'
    
    def nome_arquivo_display(self, obj):
        """Exibe o nome do arquivo com ícone baseado na extensão."""
        extensao = obj.extensao_arquivo or 'file'
        icon_map = {
            'pdf': ('fa-file-pdf', 'red'),
            'doc': ('fa-file-word', 'blue'),
            'docx': ('fa-file-word', 'blue'),
            'xls': ('fa-file-excel', 'green'),
            'xlsx': ('fa-file-excel', 'green'),
            'jpg': ('fa-file-image', 'orange'),
            'jpeg': ('fa-file-image', 'orange'),
            'png': ('fa-file-image', 'orange'),
            'zip': ('fa-file-archive', 'purple'),
            'rar': ('fa-file-archive', 'purple'),
        }
        
        icon_class, color = icon_map.get(extensao, ('fa-file', 'gray'))
        
        return format_html(
            '<i class="fas {}" style="color: {};"></i> {}<br><small style="color: #666;">{}</small>',
            icon_class, color, obj.nome_arquivo, obj.tamanho_arquivo
        )
    nome_arquivo_display.short_description = 'Arquivo'
    
    def status_notificacao(self, obj):
        """Exibe status visual da notificação."""
        if obj.notificacao_enviada:
            return format_html(
                '<span style="color: green;">✅ Enviado</span><br>'
                '<small style="color: #666;">{}</small>',
                obj.data_notificacao.strftime('%d/%m/%Y %H:%M') if obj.data_notificacao else ''
            )
        return format_html('<span style="color: orange;">⏳ Pendente</span>')
    status_notificacao.short_description = 'Notificação'
    
    def status_visualizacao(self, obj):
        """Exibe status visual da visualização."""
        if obj.visualizado:
            return format_html(
                '<span style="color: green;">👁️ Visualizado</span><br>'
                '<small style="color: #666;">{}</small>',
                obj.data_visualizacao.strftime('%d/%m/%Y %H:%M') if obj.data_visualizacao else ''
            )
        return format_html('<span style="color: gray;">👁️‍🗨️ Não visualizado</span>')
    status_visualizacao.short_description = 'Visualização'
    
    def get_queryset(self, request):
        """Otimiza consultas incluindo relacionamentos."""
        qs = super().get_queryset(request)
        return qs.select_related('cliente', 'enviado_por')
    
    def save_model(self, request, obj, form, change):
        """
        Preenche automaticamente o campo enviado_por.
        O signal vai disparar o envio do e-mail automaticamente.
        """
        if not obj.enviado_por:
            obj.enviado_por = request.user
        
        super().save_model(request, obj, form, change)
        
        # Mensagem de feedback
        if not change:  # Se é criação
            messages.success(
                request,
                f'Documento "{obj.titulo}" criado com sucesso! '
                f'Uma notificação por e-mail será enviada automaticamente para {obj.cliente.email}'
            )
