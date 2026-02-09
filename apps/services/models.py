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
        ('mei', 'MEI - Contabilidade'),
    ]
    
    nome = models.CharField(max_length=100, help_text="Nome do plano (ex: Bronze, Prata, Ouro)")
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='servicos')
    preco = models.DecimalField(max_digits=10, decimal_places=2, help_text="Preço mensal do plano")
    preco_antigo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Preço anterior (para mostrar desconto)")
    descricao = models.TextField(help_text="Breve descrição do plano")
    features_included = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Recursos Incluídos ✅",
        help_text='Lista de recursos INCLUÍDOS no plano. Exemplo: ["Contabilidade Completa", "Certificado Digital", "Suporte por WhatsApp"]'
    )
    features_excluded = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Recursos NÃO Incluídos ❌",
        help_text='Lista de recursos NÃO incluídos no plano. Exemplo: ["Folha de Pagamentos", "Consultoria Tributária"]'
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
    
    @property
    def features(self):
        """Combina features incluídas e excluídas em uma lista para o template"""
        combined = []
        for feature in (self.features_included or []):
            combined.append({'feature': feature, 'included': True})
        for feature in (self.features_excluded or []):
            combined.append({'feature': feature, 'included': False})
        return combined
    
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
    ]
    
    GOV_BR_NIVEL_CHOICES = [
        ('bronze', 'Bronze'),
        ('prata', 'Prata'),
        ('ouro', 'Ouro'),
    ]
    
    # Metadados
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='processos_abertura')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='rascunho')
    etapa_atual = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(8)])
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
    iptu_imovel = models.FileField(upload_to='processos_abertura/documentos/', blank=True, null=True, verbose_name="Inscrição Imobiliária/IPTU")
    
    # ETAPA 6: Informações Fiscais
    tipo_atividade = models.CharField(max_length=20, choices=TIPO_ATIVIDADE_CHOICES, blank=True, null=True)
    usa_nota_fiscal = models.BooleanField(default=False)
    precisa_alvara = models.BooleanField(default=False)
    deseja_conta_pj = models.BooleanField(default=False)
    
    # ETAPA 7: Dados de Acesso a Portais (REMOVIDO DO FLUXO, MANTIDO NO MODELO POR COMPATIBILIDADE)
    gov_br_nivel = models.CharField(max_length=10, choices=GOV_BR_NIVEL_CHOICES, blank=True, null=True)
    gov_br_cpf = models.CharField(max_length=14, blank=True, null=True)
    gov_br_senha = models.CharField(max_length=200, blank=True, null=True)  # Será encriptada
    
    # ETAPA 8: Assinatura e Termos
    aceite_termos = models.BooleanField(default=False)
    declaracao_veracidade = models.BooleanField(default=False)
    assinatura_digital = models.TextField(blank=True, null=True)  # Base64 da assinatura
    data_assinatura = models.DateTimeField(blank=True, null=True)
    
    # ETAPA 9: Pagamento
    plano_selecionado = models.ForeignKey('Plano', on_delete=models.SET_NULL, null=True, blank=True)
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


class SolicitacaoAberturaMEI(models.Model):
    """
    Modelo para armazenar as solicitações de abertura de MEI.
    Coleta todos os dados necessários para o processo de abertura.
    Valor fixo do serviço: R$ 129,90
    """
    
    # Status do processo
    STATUS_CHOICES = [
        ('pendente', 'Pendente Pagamento'),
        ('pago', 'Pago - Aguardando Processamento'),
        ('em_andamento', 'Em Andamento'),
        ('documentacao', 'Aguardando Documentação'),
        ('analise', 'Em Análise'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]
    
    # Formas de atuação do MEI (conforme legislação)
    FORMA_ATUACAO_CHOICES = [
        ('estabelecimento_fixo', 'Estabelecimento fixo'),
        ('internet', 'Internet'),
        ('porta_a_porta', 'Porta a porta'),
        ('televenda', 'Televenda'),
        ('correios', 'Correios'),
        ('local_fixo_fora_loja', 'Em local fixo fora da loja'),
        ('maquinas_automaticas', 'Máquinas automáticas'),
    ]
    
    # Estados brasileiros
    UF_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
    ]
    
    # Valor fixo do serviço
    VALOR_SERVICO = 129.90
    
    # Metadados
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pendente',
        verbose_name='Status'
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    # Dados pessoais (obrigatórios)
    nome_completo = models.CharField(
        max_length=200, 
        verbose_name='Nome Completo',
        help_text='Nome completo como consta no documento de identidade'
    )
    email = models.EmailField(
        verbose_name='E-mail',
        help_text='E-mail para contato e acompanhamento'
    )
    telefone = models.CharField(
        max_length=20, 
        verbose_name='Telefone',
        help_text='Telefone com DDD para contato'
    )
    cpf = models.CharField(
        max_length=14, 
        verbose_name='CPF',
        help_text='CPF no formato 000.000.000-00'
    )
    
    # Documentos (opcionais)
    rg = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name='RG',
        help_text='Número do RG'
    )
    orgao_expedidor_rg = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name='Órgão Expedidor',
        help_text='Ex: SSP, DETRAN, IFP'
    )
    uf_orgao_expedidor = models.CharField(
        max_length=2, 
        choices=UF_CHOICES, 
        blank=True, 
        null=True,
        verbose_name='UF do Órgão Expedidor'
    )
    
    # Atividades (CNAE)
    cnae_primario = models.CharField(
        max_length=255, 
        verbose_name='CNAE Primário',
        help_text='Atividade principal do MEI'
    )
    cnae_secundario = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name='CNAE Secundário',
        help_text='Atividade complementar (opcional)'
    )
    
    # Forma de atuação
    forma_atuacao = models.CharField(
        max_length=30, 
        choices=FORMA_ATUACAO_CHOICES,
        verbose_name='Forma de Atuação',
        help_text='Como o MEI vai exercer suas atividades'
    )
    
    # Capital social
    capital_social = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        blank=True, 
        null=True,
        verbose_name='Capital Social',
        help_text='Valor inicial investido no negócio (opcional)'
    )
    
    # Endereço completo
    cep = models.CharField(
        max_length=10, 
        verbose_name='CEP',
        help_text='CEP no formato 00000-000'
    )
    logradouro = models.CharField(
        max_length=200, 
        verbose_name='Logradouro',
        help_text='Rua, Avenida, etc.'
    )
    numero = models.CharField(
        max_length=20, 
        verbose_name='Número'
    )
    complemento = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name='Complemento',
        help_text='Apto, Bloco, Sala, etc. (opcional)'
    )
    bairro = models.CharField(
        max_length=100, 
        verbose_name='Bairro'
    )
    cidade = models.CharField(
        max_length=100, 
        verbose_name='Cidade'
    )
    estado = models.CharField(
        max_length=2, 
        choices=UF_CHOICES,
        verbose_name='Estado'
    )
    
    # Relacionamento com pagamento (opcional, para quando o pagamento for confirmado)
    pagamento = models.ForeignKey(
        'payments.Pagamento',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='solicitacoes_mei',
        verbose_name='Pagamento'
    )
    
    # Observações internas (para uso administrativo)
    observacoes = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Observações',
        help_text='Anotações internas sobre o processo'
    )
    
    class Meta:
        verbose_name = 'Solicitação de Abertura MEI'
        verbose_name_plural = 'Solicitações de Abertura MEI'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"MEI #{self.id} - {self.nome_completo} ({self.get_status_display()})"
    
    @property
    def valor_servico(self):
        """Retorna o valor fixo do serviço de abertura MEI"""
        return self.VALOR_SERVICO
    
    def cpf_formatado(self):
        """Retorna o CPF formatado para exibição"""
        cpf = ''.join(filter(str.isdigit, self.cpf))
        if len(cpf) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return self.cpf
    
    def telefone_formatado(self):
        """Retorna o telefone formatado para exibição"""
        tel = ''.join(filter(str.isdigit, self.telefone))
        if len(tel) == 11:
            return f"({tel[:2]}) {tel[2:7]}-{tel[7:]}"
        elif len(tel) == 10:
            return f"({tel[:2]}) {tel[2:6]}-{tel[6:]}"
        return self.telefone
    
    def endereco_completo(self):
        """Retorna o endereço formatado"""
        endereco = f"{self.logradouro}, {self.numero}"
        if self.complemento:
            endereco += f" - {self.complemento}"
        endereco += f", {self.bairro}, {self.cidade}/{self.estado} - CEP: {self.cep}"
        return endereco


class ServicoAvulso(models.Model):
    """
    Modelo para gerenciar serviços avulsos que podem ser contratados pelos clientes.
    Exemplo: Rescisão Retroativa, Regularização Fiscal, etc.
    """
    titulo = models.CharField(
        max_length=200,
        verbose_name='Título do Serviço',
        help_text='Nome do serviço (ex: Rescisão Retroativa)'
    )
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor',
        help_text='Valor do serviço em R$'
    )
    descricao = models.TextField(
        verbose_name='Descrição',
        help_text='Descrição detalhada do serviço'
    )
    icone = models.CharField(
        max_length=50,
        default='fas fa-file-alt',
        verbose_name='Ícone',
        help_text='Classe do ícone FontAwesome (ex: fas fa-file-alt)'
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name='Ativo',
        help_text='Se o serviço está disponível para contratação'
    )
    ordem = models.IntegerField(
        default=0,
        verbose_name='Ordem',
        help_text='Ordem de exibição (menor número aparece primeiro)'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Serviço Avulso'
        verbose_name_plural = 'Serviços Avulsos'
        ordering = ['ordem', 'titulo']
    
    def __str__(self):
        return f"{self.titulo} - R$ {self.valor}"


class ContratacaoServicoAvulso(models.Model):
    """
    Modelo para registrar a contratação de um serviço avulso por um cliente.
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aguardando_pagamento', 'Aguardando Pagamento'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contratacoes_servicos_avulsos',
        verbose_name='Cliente'
    )
    servico = models.ForeignKey(
        ServicoAvulso,
        on_delete=models.PROTECT,
        related_name='contratacoes',
        verbose_name='Serviço'
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name='Status'
    )
    valor_contratado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor Contratado',
        help_text='Valor do serviço no momento da contratação'
    )
    observacoes_cliente = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações do Cliente',
        help_text='Observações enviadas pelo cliente ao contratar'
    )
    observacoes_internas = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações Internas',
        help_text='Anotações internas sobre o andamento do serviço'
    )
    visualizado = models.BooleanField(
        default=False,
        verbose_name='Visualizado',
        help_text='Se a equipe já visualizou essa contratação'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    concluido_em = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Concluído em'
    )
    
    class Meta:
        verbose_name = 'Contratação de Serviço Avulso'
        verbose_name_plural = 'Contratações de Serviços Avulsos'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.email} - {self.servico.titulo}"
    
    def save(self, *args, **kwargs):
        # Se não tem valor contratado, pega do serviço
        if not self.valor_contratado:
            self.valor_contratado = self.servico.valor
        
        # Se mudou para concluído, marca a data
        if self.status == 'concluido' and not self.concluido_em:
            from django.utils import timezone
            self.concluido_em = timezone.now()
        
        super().save(*args, **kwargs)
