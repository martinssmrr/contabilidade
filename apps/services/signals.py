from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.payments.models import Pagamento
from .models import SolicitacaoAberturaMEI

@receiver(post_save, sender=Pagamento)
def atualizar_status_mei_ao_pagar(sender, instance, created, **kwargs):
    """
    Atualiza o status da Solicitação de Abertura MEI quando o pagamento for aprovado.
    """
    if instance.status == 'aprovado':
        # Busca solicitações MEI vinculadas a este pagamento
        # O related_name 'solicitacoes_mei' foi definido no model SolicitacaoAberturaMEI
        solicitacoes = instance.solicitacoes_mei.all()
        
        for solicitacao in solicitacoes:
            if solicitacao.status == 'pendente':
                solicitacao.status = 'pago'
                solicitacao.save()
                print(f"✅ Status da Solicitação MEI #{solicitacao.id} atualizado para 'pago' após aprovação do pagamento #{instance.id}")
