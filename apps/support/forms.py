from django import forms
from .models import Chamado


class ChamadoForm(forms.ModelForm):
    """Formulário para criação de Chamado (área do cliente)."""
    class Meta:
        model = Chamado
        fields = ['titulo', 'tipo_solicitacao', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_solicitacao': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo', '').strip()
        if not titulo:
            raise forms.ValidationError('O título é obrigatório.')
        return titulo


class ChamadoMessageForm(forms.Form):
    mensagem = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), required=True)
    anexo = forms.FileField(required=False)
