from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    """
    Modelo de usuário customizado para gerenciar diferentes níveis de acesso.
    
    Roles disponíveis:
    - cliente: Usuário final que contrata serviços
    - contador: Profissional de contabilidade que atende clientes
    - admin: Administrador do sistema com acesso total
    - suporte: Equipe de suporte técnico
    """
    
    ROLE_CHOICES = [
        ('cliente', 'Cliente'),
        ('contador', 'Contador'),
        ('admin', 'Administrador'),
        ('suporte', 'Suporte'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='cliente',
        verbose_name='Função'
    )
    
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone')
    cpf_cnpj = models.CharField(max_length=18, blank=True, null=True, verbose_name='CPF/CNPJ')
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
