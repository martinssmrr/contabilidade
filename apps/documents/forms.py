from django import forms
from .models import NotaFiscal, DocumentoEmpresa, ExtratoBancario


class NotaFiscalUploadForm(forms.ModelForm):
    """
    Formulário para upload de Notas Fiscais pela equipe.
    Os campos cliente e enviado_por são preenchidos automaticamente na view.
    """
    
    class Meta:
        model = NotaFiscal
        fields = ['arquivo_pdf', 'observacoes']
        widgets = {
            'arquivo_pdf': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'application/pdf',
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações internas (opcional)'
            }),
        }
        labels = {
            'arquivo_pdf': 'Arquivo da Nota Fiscal (PDF)',
            'observacoes': 'Observações'
        }
    
    def clean_arquivo_pdf(self):
        """Valida se o arquivo enviado é um PDF."""
        arquivo = self.cleaned_data.get('arquivo_pdf')
        
        if arquivo:
            # Verifica a extensão do arquivo
            if not arquivo.name.lower().endswith('.pdf'):
                raise forms.ValidationError('Por favor, envie apenas arquivos PDF.')
            
            # Verifica o tamanho do arquivo (máximo 10MB)
            if arquivo.size > 10 * 1024 * 1024:
                raise forms.ValidationError('O arquivo não pode ser maior que 10MB.')
        
        return arquivo


class DocumentoEmpresaUploadForm(forms.ModelForm):
    """
    Formulário para upload de Documentos da Empresa pela equipe.
    Os campos cliente e enviado_por são preenchidos automaticamente na view.
    """
    
    class Meta:
        model = DocumentoEmpresa
        fields = ['titulo', 'categoria', 'arquivo', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Contrato Social da Empresa'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select',
            }),
            'arquivo': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição adicional sobre o documento (opcional)'
            }),
        }
        labels = {
            'titulo': 'Título do Documento',
            'categoria': 'Categoria',
            'arquivo': 'Arquivo',
            'descricao': 'Descrição'
        }
    
    def clean_arquivo(self):
        """Valida o tamanho do arquivo."""
        arquivo = self.cleaned_data.get('arquivo')
        
        if arquivo:
            # Verifica o tamanho do arquivo (máximo 10MB)
            if arquivo.size > 10 * 1024 * 1024:
                raise forms.ValidationError('O arquivo não pode ser maior que 10MB.')
        
        return arquivo


class ExtratoBancarioUploadForm(forms.ModelForm):
    """
    Formulário para upload de Extratos Bancários pelo cliente.
    O campo cliente é preenchido automaticamente na view.
    """
    
    class Meta:
        model = ExtratoBancario
        fields = ['mes_ano', 'arquivo', 'observacoes']
        widgets = {
            'mes_ano': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'MM/AAAA (ex: 11/2024)',
                'pattern': '(0[1-9]|1[0-2])/[0-9]{4}',
                'title': 'Digite no formato MM/AAAA (ex: 11/2024)'
            }),
            'arquivo': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações sobre este extrato (opcional)'
            }),
        }
        labels = {
            'mes_ano': 'Mês/Ano do Extrato',
            'arquivo': 'Arquivo do Extrato',
            'observacoes': 'Observações'
        }
    
    def clean_mes_ano(self):
        """Valida o formato do mês/ano."""
        mes_ano = self.cleaned_data.get('mes_ano')
        
        if mes_ano:
            import re
            if not re.match(r'^(0[1-9]|1[0-2])/\d{4}$', mes_ano):
                raise forms.ValidationError('Digite no formato MM/AAAA (ex: 11/2024)')
            
            # Valida se o mês é válido
            try:
                mes, ano = mes_ano.split('/')
                mes = int(mes)
                ano = int(ano)
                
                if mes < 1 or mes > 12:
                    raise forms.ValidationError('Mês inválido. Digite um valor entre 01 e 12.')
                
                if ano < 2000 or ano > 2100:
                    raise forms.ValidationError('Ano inválido.')
            except ValueError:
                raise forms.ValidationError('Formato inválido. Use MM/AAAA.')
        
        return mes_ano
    
    def clean_arquivo(self):
        """Valida o tamanho do arquivo."""
        arquivo = self.cleaned_data.get('arquivo')
        
        if arquivo:
            # Verifica o tamanho do arquivo (máximo 15MB para extratos)
            if arquivo.size > 15 * 1024 * 1024:
                raise forms.ValidationError('O arquivo não pode ser maior que 15MB.')
        
        return arquivo
