from django.core.management.base import BaseCommand
from apps.services.models import SolicitacaoAberturaMEI

class Command(BaseCommand):
    help = 'Corrige status de solicitações MEI com pagamento aprovado'

    def handle(self, *args, **options):
        self.stdout.write("Verificando solicitações MEI...")
        
        solicitacoes = SolicitacaoAberturaMEI.objects.select_related('pagamento').all()
        count = 0
        
        for sol in solicitacoes:
            if sol.pagamento and sol.pagamento.status == 'aprovado' and sol.status == 'pendente':
                sol.status = 'pago'
                sol.save()
                count += 1
                self.stdout.write(self.style.SUCCESS(f"Solicitação #{sol.id} atualizada para 'pago'"))
            elif sol.pagamento:
               self.stdout.write(f"Solicitação #{sol.id}: Status={sol.status}, Pagamento={sol.pagamento.status}")
        
        self.stdout.write(self.style.SUCCESS(f"Concluído! {count} solicitações atualizadas."))
