import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vetorial_project.settings')

# Hack to avoid logging permission error in Docker
import logging.config
original_dictConfig = logging.config.dictConfig
def no_op_dictConfig(config):
    # Filter out file handlers that might fail
    if 'handlers' in config:
        for handler in list(config['handlers'].keys()):
            if 'filename' in config['handlers'][handler]:
                 # Remove file handlers to avoid permission errors
                 del config['handlers'][handler]
    
    # Try to configure with safe handlers, or just pass
    try:
        original_dictConfig(config)
    except Exception:
        pass

logging.config.dictConfig = no_op_dictConfig

django.setup()

from apps.services.models import Plano

def populate_mei_plans():
    print("Creating MEI Plans...")

    # Básico
    p1, created = Plano.objects.get_or_create(
        nome="Básico",
        categoria="mei",
        defaults={
            "preco": 29.90,
            "descricao": "Ideal para quem está começando.",
            "features_included": [
                "Boleto DAS por mês",
                "Até 01 Nota Fiscal por mês",
                "Inscrição estadual",
                "Declaração MEI",
                "Alteração e Cadastro DET",
                "Consultoria Compra de Carro",
                "Consultoria Empréstimo Bancário"
            ],
            "features_excluded": [
                "Regularização com Parcelamento",
                "Alterar MEI",
                "Alvará de Funcionamento",
                "Certidão Negativa de Débitos",
                "Certificado Digital",
                "Certificado MEI - CCMEI",
                "Contrato Social",
                "Desenquadramento MEI",
                "Reenquadramento MEI",
                "Advogado para Entrada nos Benefícios",
                "Controle Fiscal (Pendências com Receita Federal)",
                "Suporte Técnico com Contador 24 horas"
            ],
            "ordem": 1
        }
    )
    if not created:
        print(f"Plan {p1.nome} already exists. Updating price...")
        p1.preco = 29.90
        p1.save()

    # Secundário
    p2, created = Plano.objects.get_or_create(
        nome="Secundário",
        categoria="mei",
        defaults={
            "preco": 59.90,
            "descricao": "Para quem precisa de mais flexibilidade.",
            "features_included": [
                "Boleto DAS por mês",
                "Até 05 Nota Fiscal por mês",
                "Inscrição estadual",
                "Declaração MEI",
                "Alteração e Cadastro DET",
                "Consultoria Compra de Carro",
                "Consultoria Empréstimo Bancário"
            ],
            "features_excluded": [
                "Regularização com Parcelamento",
                "Alterar MEI",
                "Alvará de Funcionamento",
                "Certidão Negativa de Débitos",
                "Certificado Digital",
                "Certificado MEI - CCMEI",
                "Contrato Social",
                "Desenquadramento MEI",
                "Reenquadramento MEI",
                "Advogado para Entrada nos Benefícios",
                "Controle Fiscal (Pendências com Receita Federal)",
                "Suporte Técnico com Contador 24 horas"
            ],
            "ordem": 2
        }
    )
    if not created:
         print(f"Plan {p2.nome} already exists. Updating price...")
         p2.preco = 59.90
         p2.save()

    # Premium
    p3, created = Plano.objects.get_or_create(
        nome="Premium",
        categoria="mei",
        defaults={
            "preco": 79.90,
            "descricao": "A solução completa para o seu negócio.",
            "features_included": [
                "Boleto DAS por mês",
                "Nota Fiscal ilimitada",
                "Inscrição estadual",
                "Alteração e Cadastro DET",
                "Declaração MEI",
                "Consultoria Compra de Carro",
                "Consultoria Empréstimo Bancário",
                "Regularização com Parcelamento",
                "Alterar MEI",
                "Alvará de Funcionamento",
                "Certidão Negativa de Débitos",
                "Certificado Digital",
                "Certificado MEI - CCMEI",
                "Contrato Social",
                "Desenquadramento MEI",
                "Reenquadramento MEI",
                "Advogado para Entrada nos Benefícios",
                "Controle Fiscal (Pendências com Receita Federal)",
                "Suporte Técnico com Contador 24 horas"
            ],
            "features_excluded": [],
            "destaque": True,
            "ordem": 3
        }
    )
    if not created:
         print(f"Plan {p3.nome} already exists. Updating price...")
         p3.preco = 79.90
         p3.destaque = True
         p3.save()
         
    print("Plans created/updated successfully.")

if __name__ == "__main__":
    populate_mei_plans()
