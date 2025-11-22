from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Plano(models.Model):
    """
    Modelo para gerenciar os planos de serviço oferecidos pela empresa.
    Usado tanto para exibição na homepage quanto para seleção no wizard de abertura.
    """
    CATEGORIA_CHOICES = [
        ('servicos', 'Serviços'),
        ('comercio', 'Comércio'),
        ('abertura', 'Abertura de Empresa'),
    ]
    
    nome = models.CharField(max_length=100, help_text="Nome do plano (ex: Bronze, Prata, Ouro)")
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='servicos')
    preco = models.DecimalField(max_digits=10, decimal_places=2, help_text="Preço mensal do plano")
    preco_antigo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Preço anterior (para mostrar desconto)")
    descricao = models.TextField(help_text="Breve descrição do plano")
    features = models.JSONField(
        default=list,
        help_text="Lista de características/benefícios do plano. Ex: ['Contabilidade completa', 'Certificado digital']"
    )
    mercadopago_price_id = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="ID do preço/produto no Mercado Pago para integração de pagamento"
    )
    ativo = models.BooleanField(default=True, help_text="Se o plano está ativo e disponível para contratação")
    destaque = models.BooleanField(default=False, help_text="Marcar como 'Mais Popular' ou em destaque")
    ordem = models.IntegerField(default=0, help_text="Ordem de exibição (menor número aparece primeiro)")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['categoria', 'ordem', 'preco']
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
    
    def __str__(self):
        return f"{self.nome} - {self.get_categoria_display()} (R$ {self.preco})"
    
    def tem_desconto(self):
        """Verifica se o plano tem preço antigo configurado (está em promoção)"""
        return self.preco_antigo and self.preco_antigo > self.preco
    
    def percentual_desconto(self):
        """Calcula o percentual de desconto se houver"""
        if self.tem_desconto():
            desconto = ((self.preco_antigo - self.preco) / self.preco_antigo) * 100
            return round(desconto, 0)
        return 0

class ProcessoAbertura(models.Model):
    """
    Modelo principal para armazenar todos os dados do processo de abertura de empresa
    """
    # Estados do processo
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('em_andamento', 'Em Andamento'),
        ('aguardando_documentos', 'Aguardando Documentos'),
        ('aguardando_pagamento', 'Aguardando Pagamento'),
        ('em_analise', 'Em Análise'),
        ('aprovado', 'Aprovado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]
    
    TIPO_SOCIETARIO_CHOICES = [
        ('MEI', 'MEI - Microempreendedor Individual'),
        ('ME', 'ME - Microempresa'),
        ('EPP', 'EPP - Empresa de Pequeno Porte'),
        ('LTDA', 'LTDA - Sociedade Limitada'),
    ]
    
    ESTADO_CIVIL_CHOICES = [
        ('solteiro', 'Solteiro(a)'),
        ('casado', 'Casado(a)'),
        ('divorciado', 'Divorciado(a)'),
        ('viuvo', 'Viúvo(a)'),
        ('uniao_estavel', 'União Estável'),
    ]
    
    UF_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
    ]
    
    FORMA_ATUACAO_CHOICES = [
        ('online', 'Online'),
        ('presencial', 'Presencial'),
        ('ambos', 'Ambos'),
    ]
    
    LOCAL_EMPRESA_CHOICES = [
        ('residencial', 'Residencial'),
        ('comercial', 'Comercial'),
    ]
    
    REGIME_TRIBUTARIO_CHOICES = [
        ('simples_nacional', 'Simples Nacional'),
        ('lucro_presumido', 'Lucro Presumido'),
        ('lucro_real', 'Lucro Real'),
    ]
    
    TIPO_ATIVIDADE_CHOICES = [
        ('servico', 'Serviço'),
        ('comercio', 'Comércio'),
        ('industria', 'Indústria'),
        ('misto', 'Misto'),
    ]
    
    GOV_BR_NIVEL_CHOICES = [
        ('bronze', 'Bronze'),
        ('prata', 'Prata'),
        ('ouro', 'Ouro'),
    ]
    
    # Metadados
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='processos_abertura')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='rascunho')
    etapa_atual = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(9)])
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    concluido_em = models.DateTimeField(null=True, blank=True)
    
    # ETAPA 1: Dados Pessoais do Responsável
    nome_completo = models.CharField(max_length=200, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    orgao_emissor = models.CharField(max_length=20, blank=True, null=True)
    uf_emissao = models.CharField(max_length=2, choices=UF_CHOICES, blank=True, null=True)
    telefone_whatsapp = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES, blank=True, null=True)
    nome_mae = models.CharField(max_length=200, blank=True, null=True)
    profissao = models.CharField(max_length=100, blank=True, null=True)
    
    # ETAPA 2: Endereço Residencial
    cep = models.CharField(max_length=10, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, choices=UF_CHOICES, blank=True, null=True)
    
    # ETAPA 3: Dados da Empresa
    tipo_societario = models.CharField(max_length=10, choices=TIPO_SOCIETARIO_CHOICES, blank=True, null=True)
    
    # Campos para MEI
    nome_fantasia_mei = models.CharField(max_length=200, blank=True, null=True)
    area_atuacao_mei = models.TextField(blank=True, null=True)
    cnae_principal_mei = models.CharField(max_length=20, blank=True, null=True)
    cnaes_secundarios_mei = models.TextField(blank=True, null=True)
    forma_atuacao_mei = models.CharField(max_length=20, choices=FORMA_ATUACAO_CHOICES, blank=True, null=True)
    local_empresa_mei = models.CharField(max_length=20, choices=LOCAL_EMPRESA_CHOICES, blank=True, null=True)
    
    # Campos para ME/EPP/LTDA
    razao_social = models.CharField(max_length=200, blank=True, null=True)
    nome_fantasia_me = models.CharField(max_length=200, blank=True, null=True)
    cnae_principal_me = models.CharField(max_length=20, blank=True, null=True)
    cnaes_secundarios_me = models.TextField(blank=True, null=True)
    capital_social = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    quantidade_socios = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1)])
    regime_tributario = models.CharField(max_length=30, choices=REGIME_TRIBUTARIO_CHOICES, blank=True, null=True)
    endereco_comercial_diferente = models.BooleanField(default=False)
    
    # Endereço Comercial (se diferente)
    cep_comercial = models.CharField(max_length=10, blank=True, null=True)
    endereco_comercial = models.CharField(max_length=200, blank=True, null=True)
    numero_comercial = models.CharField(max_length=10, blank=True, null=True)
    complemento_comercial = models.CharField(max_length=100, blank=True, null=True)
    bairro_comercial = models.CharField(max_length=100, blank=True, null=True)
    cidade_comercial = models.CharField(max_length=100, blank=True, null=True)
    estado_comercial = models.CharField(max_length=2, choices=UF_CHOICES, blank=True, null=True)
    
    # ETAPA 5: Upload de Documentos
    doc_identidade_frente = models.ImageField(upload_to='processos_abertura/documentos/', blank=True, null=True)
    doc_identidade_verso = models.ImageField(upload_to='processos_abertura/documentos/', blank=True, null=True)
    comprovante_residencia = models.FileField(upload_to='processos_abertura/documentos/', blank=True, null=True)
    selfie_com_documento = models.ImageField(upload_to='processos_abertura/documentos/', blank=True, null=True)
    
    # ETAPA 6: Informações Fiscais
    tipo_atividade = models.CharField(max_length=20, choices=TIPO_ATIVIDADE_CHOICES, blank=True, null=True)
    usa_nota_fiscal = models.BooleanField(default=False)
    precisa_alvara = models.BooleanField(default=False)
    deseja_conta_pj = models.BooleanField(default=False)
    
    # ETAPA 7: Dados de Acesso a Portais
    gov_br_nivel = models.CharField(max_length=10, choices=GOV_BR_NIVEL_CHOICES, blank=True, null=True)
    gov_br_cpf = models.CharField(max_length=14, blank=True, null=True)
    gov_br_senha = models.CharField(max_length=200, blank=True, null=True)  # Será encriptada
    
    # ETAPA 8: Assinatura e Termos
    aceite_termos = models.BooleanField(default=False)
    declaracao_veracidade = models.BooleanField(default=False)
    assinatura_digital = models.TextField(blank=True, null=True)  # Base64 da assinatura
    data_assinatura = models.DateTimeField(blank=True, null=True)
    
    # ETAPA 9: Pagamento
    plano_selecionado = models.ForeignKey('Plan', on_delete=models.SET_NULL, null=True, blank=True)
    cupom_desconto = models.CharField(max_length=50, blank=True, null=True)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    data_pagamento = models.DateTimeField(blank=True, null=True)
    pagamento_confirmado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Processo de Abertura'
        verbose_name_plural = 'Processos de Abertura'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"Processo #{self.id} - {self.nome_completo or 'Sem nome'} - {self.get_status_display()}"


class Socio(models.Model):
    """
    Modelo para armazenar dados dos sócios (para ME/EPP/LTDA)
    """
    ESTADO_CIVIL_CHOICES = ProcessoAbertura.ESTADO_CIVIL_CHOICES
    
    processo = models.ForeignKey(ProcessoAbertura, on_delete=models.CASCADE, related_name='socios')
    nome_completo = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14)
    rg = models.CharField(max_length=20)
    estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES)
    endereco_completo = models.TextField()
    percentual_participacao = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(100.00)]
    )
    
    class Meta:
        verbose_name = 'Sócio'
        verbose_name_plural = 'Sócios'
    
    def __str__(self):
        return f"{self.nome_completo} - {self.percentual_participacao}%"


class Service(models.Model):
    """
    Modelo para serviços avulsos de contabilidade.
    Exemplos: Abertura de Empresa, Declaração de IR, Alteração Contratual, etc.
    """
    nome = models.CharField(max_length=200, verbose_name='Nome do Serviço')
    descricao = models.TextField(verbose_name='Descrição')
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"


class Plan(models.Model):
    """
    Modelo para planos de assinatura (mensal/anual).
    Exemplos: Plano MEI Mensal, Plano Empresarial Anual, etc.
    """
    PERIODO_CHOICES = [
        ('mensal', 'Mensal'),
        ('anual', 'Anual'),
    ]
    
    nome = models.CharField(max_length=200, verbose_name='Nome do Plano')
    descricao = models.TextField(verbose_name='Descrição')
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    periodo = models.CharField(max_length=10, choices=PERIODO_CHOICES, default='mensal', verbose_name='Período')
    caracteristicas = models.TextField(help_text='Uma característica por linha', verbose_name='Características')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
        ordering = ['preco']
    
    def __str__(self):
        return f"{self.nome} ({self.get_periodo_display()}) - R$ {self.preco}"


class Subscription(models.Model):
    """
    Modelo para controlar as assinaturas ativas dos clientes.
    """
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('cancelada', 'Cancelada'),
        ('suspensa', 'Suspensa'),
        ('expirada', 'Expirada'),
    ]
    
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assinaturas')
    plano = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='assinaturas')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativa', verbose_name='Status')
    data_inicio = models.DateField(verbose_name='Data de Início')
    data_fim = models.DateField(null=True, blank=True, verbose_name='Data de Término')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Assinatura'
        verbose_name_plural = 'Assinaturas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.cliente.username} - {self.plano.nome} ({self.status})"


class CategoriaCNAE(models.Model):
    """
    Modelo para categorizar CNAEs por área de atuação
    """
    nome = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name='Nome da Categoria',
        help_text='Ex: Consultoria, Software, Educação'
    )
    ordem = models.IntegerField(
        default=0,
        verbose_name='Ordem de Exibição',
        help_text='Menor número aparece primeiro'
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Categoria CNAE'
        verbose_name_plural = 'Categorias CNAE'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome
    
    def total_cnaes(self):
        """Retorna o total de CNAEs nesta categoria"""
        return self.cnaes.count()
    total_cnaes.short_description = 'Total de CNAEs'


class CNAE(models.Model):
    """
    Modelo para armazenar CNAEs (Classificação Nacional de Atividades Econômicas)
    """
    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código CNAE',
        help_text='Ex: 6201-5/01, 8599-6/99'
    )
    descricao = models.TextField(
        verbose_name='Descrição',
        help_text='Descrição completa da atividade econômica'
    )
    categoria = models.ForeignKey(
        CategoriaCNAE,
        on_delete=models.CASCADE,
        related_name='cnaes',
        verbose_name='Categoria'
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name='Ativo',
        help_text='Se o CNAE está ativo para consulta'
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'CNAE'
        verbose_name_plural = 'CNAEs'
        ordering = ['categoria__ordem', 'categoria__nome', 'codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descricao[:50]}"
