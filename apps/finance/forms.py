from django import forms
from .models import Transaction, Subcategory, Account, ScheduledTransaction

class ScheduledTransactionForm(forms.ModelForm):
    class Meta:
        model = ScheduledTransaction
        fields = ['type', 'account', 'description', 'value', 'due_date', 'is_recurring']
        widgets = {
            'type': forms.HiddenInput(), # Será definido via view/contexto
            'account': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Fornecedor ou Cliente'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_recurring': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user)

class TreeNodeChoiceField(forms.ModelChoiceField):
    """Campo Choice customizado para exibir hierarquia no select"""
    def label_from_instance(self, obj):
        level = obj.get_level()
        prefix = "&nbsp;&nbsp;&nbsp;&nbsp;" * level
        return f"{prefix}{obj.code} - {obj.name}" if obj.code else f"{prefix}{obj.name}"

class TransactionForm(forms.ModelForm):
    account = TreeNodeChoiceField(queryset=Account.objects.none(), widget=forms.Select(attrs={'class': 'form-select'}))
    
    class Meta:
        model = Transaction
        fields = ['date', 'account', 'value', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Permite lançamento em qualquer conta (Sintética ou Analítica) conforme solicitado
        self.fields['account'].queryset = Account.objects.filter(
            user=user
        ).order_by('code')

class AccountForm(forms.ModelForm):
    parent = TreeNodeChoiceField(
        queryset=Account.objects.none(), 
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Conta Pai'
    )

    class Meta:
        model = Account
        fields = ['parent', 'name', 'code', 'is_synthetic']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1.1.01'}),
            'is_synthetic': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Para escolher o pai, pode ser qualquer conta SINTÉTICA
        self.fields['parent'].queryset = Account.objects.filter(
            user=user,
            is_synthetic=True
        ).order_by('code')

