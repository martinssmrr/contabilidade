from django import forms
from django.core.validators import RegexValidator
from django.forms import formset_factory
from .models import ProcessoAbertura, Socio, SolicitacaoAberturaMEI
from .cnae_choices import MEI_CNAES


# Validators
cpf_validator = RegexValidator(
    regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
    message='CPF deve estar no formato: 000.000.000-00'
)

telefone_validator = RegexValidator(
    regex=r'^\(\d{2}\) \d{4,5}-\d{4}$',
    message='Telefone deve estar no formato: (00) 00000-0000'
)


class Etapa1DadosPessoaisForm(forms.ModelForm):
    """Etapa 1: Dados Pessoais do Responsável"""
    
    class Meta:
        model = ProcessoAbertura
        fields = [
            'nome_completo', 'data_nascimento', 'cpf', 'rg', 'orgao_emissor',
            'uf_emissao', 'telefone_whatsapp', 'email', 'estado_civil',
            'nome_mae', 'profissao'
        ]
        widgets = {
            'nome_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu nome completo'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
                'data-mask': '000.000.000-00'
            }),
            'rg': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu RG'
            }),
            'orgao_emissor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: SSP, DETRAN'
            }),
            'uf_emissao': forms.Select(attrs={'class': 'form-select'}),
            'telefone_whatsapp': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000',
                'data-mask': '(00) 00000-0000'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'seuemail@exemplo.com'
            }),
            'estado_civil': forms.Select(attrs={'class': 'form-select'}),
            'nome_mae': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo da mãe'
            }),
            'profissao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sua profissão atual'
            }),
        }


class Etapa2EnderecoForm(forms.ModelForm):
    """Etapa 2: Endereço Residencial"""
    
    class Meta:
        model = ProcessoAbertura
        fields = ['cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado']
        widgets = {
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-000',
                'data-mask': '00000-000',
                'id': 'id_cep'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rua, Avenida, etc.',
                'id': 'id_endereco'
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número'
            }),
            'complemento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apto, Bloco, etc. (opcional)'
            }),
            'bairro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bairro',
                'id': 'id_bairro'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade',
                'id': 'id_cidade'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_estado'
            }),
        }


class Etapa3DadosEmpresaForm(forms.ModelForm):
    """Etapa 3: Dados da Empresa"""
    
    class Meta:
        model = ProcessoAbertura
        fields = [
            'tipo_societario',
            # Campos MEI
            'nome_fantasia_mei', 'area_atuacao_mei', 'cnae_principal_mei',
            'cnaes_secundarios_mei', 'forma_atuacao_mei', 'local_empresa_mei',
            # Campos ME/EPP/LTDA
            'razao_social', 'nome_fantasia_me', 'cnae_principal_me',
            'cnaes_secundarios_me', 'capital_social', 'quantidade_socios',
            'regime_tributario',
            # Endereço Comercial
            'cep_comercial', 'endereco_comercial', 'numero_comercial',
            'complemento_comercial', 'bairro_comercial', 'cidade_comercial',
            'estado_comercial'
        ]
        widgets = {
            'tipo_societario': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_tipo_societario'
            }),
            # MEI
            'nome_fantasia_mei': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome fantasia da empresa'
            }),
            'area_atuacao_mei': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva a área de atuação'
            }),
            'cnae_principal_mei': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código CNAE principal'
            }),
            'cnaes_secundarios_mei': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'CNAEs secundários (opcional)'
            }),
            'forma_atuacao_mei': forms.Select(attrs={'class': 'form-select'}),
            'local_empresa_mei': forms.Select(attrs={'class': 'form-select'}),
            # ME/EPP/LTDA
            'razao_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Razão social (opcional)'
            }),
            'nome_fantasia_me': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome fantasia'
            }),
            'cnae_principal_me': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código CNAE principal'
            }),
            'cnaes_secundarios_me': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'CNAEs secundários (opcional)'
            }),
            'capital_social': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 10000.00',
                'step': '0.01'
            }),
            'quantidade_socios': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Número de sócios'
            }),
            'regime_tributario': forms.Select(attrs={'class': 'form-select'}),
            # Endereço Comercial
            'cep_comercial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-000',
                'data-mask': '00000-000'
            }),
            'endereco_comercial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço'
            }),
            'numero_comercial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número'
            }),
            'complemento_comercial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Complemento (opcional)'
            }),
            'bairro_comercial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bairro'
            }),
            'cidade_comercial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade'
            }),
            'estado_comercial': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_societario'].required = True


class SocioForm(forms.ModelForm):
    """Formulário para cada sócio"""
    
    class Meta:
        model = Socio
        fields = ['nome_completo', 'cpf', 'rg', 'estado_civil', 'endereco_completo', 'percentual_participacao']
        widgets = {
            'nome_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do sócio'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
                'data-mask': '000.000.000-00'
            }),
            'rg': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'RG'
            }),
            'estado_civil': forms.Select(attrs={'class': 'form-select'}),
            'endereco_completo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Endereço completo'
            }),
            'percentual_participacao': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01',
                'max': '100.00'
            }),
        }


# Formset para múltiplos sócios
SocioFormSet = formset_factory(SocioForm, extra=1, can_delete=True)


class Etapa5DocumentosForm(forms.ModelForm):
    """Etapa 5: Upload de Documentos"""
    
    class Meta:
        model = ProcessoAbertura
        fields = ['doc_identidade_frente', 'doc_identidade_verso', 'comprovante_residencia', 'selfie_com_documento', 'iptu_imovel']
        widgets = {
            'doc_identidade_frente': forms.FileInput(attrs={
                'class': 'form-control filepond',
                'accept': 'image/*'
            }),
            'doc_identidade_verso': forms.FileInput(attrs={
                'class': 'form-control filepond',
                'accept': 'image/*'
            }),
            'comprovante_residencia': forms.FileInput(attrs={
                'class': 'form-control filepond',
                'accept': 'image/*,.pdf'
            }),
            'selfie_com_documento': forms.FileInput(attrs={
                'class': 'form-control filepond',
                'accept': 'image/*'
            }),
            'iptu_imovel': forms.FileInput(attrs={
                'class': 'form-control filepond',
                'accept': 'image/*,.pdf'
            }),
        }


class Etapa6InformacoesFiscaisForm(forms.ModelForm):
    """Etapa 6: Informações Fiscais"""
    
    class Meta:
        model = ProcessoAbertura
        fields = ['tipo_atividade', 'usa_nota_fiscal', 'precisa_alvara', 'deseja_conta_pj']
        widgets = {
            'tipo_atividade': forms.Select(attrs={'class': 'form-select'}),
            'usa_nota_fiscal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'precisa_alvara': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'deseja_conta_pj': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class Etapa8AssinaturaForm(forms.ModelForm):
    """Etapa 7: Assinatura e Termos"""
    
    class Meta:
        model = ProcessoAbertura
        fields = ['aceite_termos', 'declaracao_veracidade', 'assinatura_digital']
        widgets = {
            'aceite_termos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'declaracao_veracidade': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'assinatura_digital': forms.HiddenInput(),
        }


class Etapa8RevisaoForm(forms.Form):
    """Etapa 8: Revisão e Conclusão (Sem campos, apenas confirmação)"""
    pass


# =============================================================================
# FORMULÁRIO DE ABERTURA MEI (Página /abrir-mei/)
# =============================================================================

class AberturaMEIForm(forms.ModelForm):
    """
    Formulário para coleta de dados de abertura de MEI.
    Inclui validações de CPF, telefone e campos obrigatórios.
    Valor do serviço: R$ 129,90
    """
    
    class Meta:
        from .models import SolicitacaoAberturaMEI
        model = SolicitacaoAberturaMEI
        fields = [
            # Dados pessoais obrigatórios
            'nome_completo', 'email', 'telefone', 'cpf',
            # Documentos opcionais
            'rg', 'orgao_expedidor_rg', 'uf_orgao_expedidor',
            # Atividades
            'cnae_primario', 'cnae_secundario',
            # Forma de atuação
            'forma_atuacao',
            # Capital social
            'capital_social',
            # Endereço
            'cep', 'logradouro', 'numero', 'complemento', 
            'bairro', 'cidade', 'estado',
        ]
        widgets = {
            # Dados pessoais
            'nome_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu nome completo',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'seuemail@exemplo.com',
                'required': True,
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000',
                'data-mask': '(00) 00000-0000',
                'required': True,
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
                'data-mask': '000.000.000-00',
                'required': True,
            }),
            # Documentos
            'rg': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número do RG',
            }),
            'orgao_expedidor_rg': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: SSP, DETRAN',
            }),
            'uf_orgao_expedidor': forms.Select(attrs={
                'class': 'form-select',
            }),
            # Atividades
            'cnae_primario': forms.Select(choices=MEI_CNAES, attrs={ 
                'class': 'form-select select2-cnae',
                'required': True, 
            }),
            'cnae_secundario': forms.Select(choices=MEI_CNAES, attrs={ 
                'class': 'form-select select2-cnae',
            }),
            # Forma de atuação
            'forma_atuacao': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            # Capital social
            'capital_social': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 5000.00',
                'step': '0.01',
                'min': '0',
            }),
            # Endereço
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-000',
                'data-mask': '00000-000',
                'id': 'mei_cep',
                'required': True,
            }),
            'logradouro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rua, Avenida, etc.',
                'id': 'mei_logradouro',
                'required': True,
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número',
                'required': True,
            }),
            'complemento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apto, Bloco, Sala (opcional)',
            }),
            'bairro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bairro',
                'id': 'mei_bairro',
                'required': True,
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade',
                'id': 'mei_cidade',
                'required': True,
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select',
                'id': 'mei_estado',
                'required': True,
            }),
        }
        labels = {
            'nome_completo': 'Nome Completo *',
            'email': 'E-mail *',
            'telefone': 'Telefone *',
            'cpf': 'CPF *',
            'rg': 'RG',
            'orgao_expedidor_rg': 'Órgão Expedidor',
            'uf_orgao_expedidor': 'UF do Órgão',
            'cnae_primario': 'Atividade Principal (CNAE) *',
            'cnae_secundario': 'Atividade Secundária',
            'forma_atuacao': 'Forma de Atuação *',
            'capital_social': 'Capital Social',
            'cep': 'CEP *',
            'logradouro': 'Logradouro *',
            'numero': 'Número *',
            'complemento': 'Complemento',
            'bairro': 'Bairro *',
            'cidade': 'Cidade *',
            'estado': 'Estado *',
        }
        help_texts = {
            'cpf': 'Informe seu CPF válido',
            'cnae_primario': 'Selecione sua atividade principal',
            'capital_social': 'Valor inicial investido no negócio (opcional)',
        }
    
    def clean_cpf(self):
        """Validação do CPF"""
        cpf = self.cleaned_data.get('cpf', '')
        # Remove caracteres não numéricos
        cpf_numeros = ''.join(filter(str.isdigit, cpf))
        
        if not cpf_numeros:
            return ""

        if len(cpf_numeros) != 11:
            raise forms.ValidationError('CPF deve conter 11 dígitos.')
        
        # Validação do dígito verificador
        if not self._validar_cpf(cpf_numeros):
            raise forms.ValidationError('CPF inválido. Verifique os dígitos informados.')
        
        # Retorna o CPF formatado
        return f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"
    
    def _validar_cpf(self, cpf):
        """
        Algoritmo de validação de CPF brasileiro.
        Retorna True se o CPF é válido, False caso contrário.
        """
        # Verifica se todos os dígitos são iguais (CPF inválido)
        if cpf == cpf[0] * 11:
            return False
        
        # Validação do primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        if int(cpf[9]) != digito1:
            return False
        
        # Validação do segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        return int(cpf[10]) == digito2
    
    def clean_telefone(self):
        """Validação do telefone"""
        telefone = self.cleaned_data.get('telefone', '')
        # Remove caracteres não numéricos
        telefone_numeros = ''.join(filter(str.isdigit, telefone))
        
        if len(telefone_numeros) < 10 or len(telefone_numeros) > 11:
            raise forms.ValidationError('Telefone deve ter 10 ou 11 dígitos (com DDD).')
        
        return telefone
    
    def clean_email(self):
        """Validação do e-mail"""
        email = self.cleaned_data.get('email', '').lower().strip()
        
        if not email:
            raise forms.ValidationError('E-mail é obrigatório.')
        
        # Validação adicional de formato
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise forms.ValidationError('Informe um e-mail válido.')
        
        return email
    
    def clean_cep(self):
        """Validação do CEP"""
        cep = self.cleaned_data.get('cep', '')
        # Remove caracteres não numéricos
        cep_numeros = ''.join(filter(str.isdigit, cep))
        
        if len(cep_numeros) != 8:
            raise forms.ValidationError('CEP deve conter 8 dígitos.')
        
        return cep
    
    def clean(self):
        """Validações adicionais do formulário"""
        cleaned_data = super().clean()
        
        # Verifica se RG foi preenchido junto com órgão expedidor
        rg = cleaned_data.get('rg')
        orgao = cleaned_data.get('orgao_expedidor_rg')
        uf_orgao = cleaned_data.get('uf_orgao_expedidor')
        
        if rg and not orgao:
            self.add_error('orgao_expedidor_rg', 'Informe o órgão expedidor do RG.')
        
        if rg and not uf_orgao:
            self.add_error('uf_orgao_expedidor', 'Informe o estado do órgão expedidor.')
        
        return cleaned_data

