from django import forms
from django.core.validators import RegexValidator
from django.forms import formset_factory
from .models import ProcessoAbertura, Socio


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
            'regime_tributario', 'endereco_comercial_diferente',
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
            'endereco_comercial_diferente': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_endereco_comercial_diferente'
            }),
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
        fields = ['doc_identidade_frente', 'doc_identidade_verso', 'comprovante_residencia', 'selfie_com_documento']
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


class Etapa7DadosAcessoForm(forms.ModelForm):
    """Etapa 7: Dados de Acesso a Portais"""
    
    class Meta:
        model = ProcessoAbertura
        fields = ['gov_br_nivel', 'gov_br_cpf', 'gov_br_senha']
        widgets = {
            'gov_br_nivel': forms.Select(attrs={'class': 'form-select'}),
            'gov_br_cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
                'data-mask': '000.000.000-00'
            }),
            'gov_br_senha': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite sua senha do Gov.br'
            }),
        }


class Etapa8AssinaturaForm(forms.ModelForm):
    """Etapa 8: Assinatura e Termos"""
    
    class Meta:
        model = ProcessoAbertura
        fields = ['aceite_termos', 'declaracao_veracidade', 'assinatura_digital']
        widgets = {
            'aceite_termos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'declaracao_veracidade': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'assinatura_digital': forms.HiddenInput(),
        }


class Etapa9PagamentoForm(forms.ModelForm):
    """Etapa 9: Pagamento"""
    
    class Meta:
        model = ProcessoAbertura
        fields = ['plano_selecionado', 'cupom_desconto']
        widgets = {
            'plano_selecionado': forms.Select(attrs={'class': 'form-select'}),
            'cupom_desconto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o cupom (opcional)'
            }),
        }
