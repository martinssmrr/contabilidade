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
        fields = ['start_date', 'end_date', 'arquivo', 'observacoes']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
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
            'start_date': 'Data Inicial',
            'end_date': 'Data Final',
            'arquivo': 'Arquivo do Extrato',
            'observacoes': 'Observações'
        }
    
    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')

        if not start or not end:
            raise forms.ValidationError('Preencha as datas inicial e final do período.')

        if start > end:
            raise forms.ValidationError('A data inicial não pode ser posterior à data final.')

        return cleaned
    
    def clean_arquivo(self):
        """Valida o tamanho do arquivo."""
        arquivo = self.cleaned_data.get('arquivo')
        
        if arquivo:
            # Verifica o tamanho do arquivo (máximo 15MB para extratos)
            if arquivo.size > 15 * 1024 * 1024:
                raise forms.ValidationError('O arquivo não pode ser maior que 15MB.')
        
        return arquivo
