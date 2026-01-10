from celery import shared_task
from django.conf import settings
from .models import BankReconciliation, Account
import ofxparse
from datetime import datetime
import os

@shared_task
def process_ofx_file(file_path, user_id):
    """
    Processa um arquivo OFX e cria registros de conciliação.
    """
    print(f"[OFX] Iniciando processamento. Path: {file_path}, UserID: {user_id}")
    
    if not os.path.exists(file_path):
        print(f"[OFX] ERRO: Arquivo não encontrado no caminho: {file_path}")
        return

    try:
        with open(file_path, 'rb') as f:
            print(f"[OFX] Arquivo aberto com sucesso. Fazendo parse...")
            ofx = ofxparse.OfxParser.parse(f)
            print(f"[OFX] Parse realizado. Conta: {ofx.account.number if hasattr(ofx.account, 'number') else 'N/A'}")
            print(f"[OFX] Total de transações encontradas: {len(ofx.account.statement.transactions)}")
        
        # Mapeamento simples de palavras-chave para sugestão
        # Isso poderia ser movido para o banco de dados futuramente
        KEYWORD_MAPPING = {
            'POSTO': 'Combustível',
            'IPIRANGA': 'Combustível',
            'SHELL': 'Combustível',
            'ALUGUEL': 'Aluguel',
            'TELEFONE': 'Telefone',
            'INTERNET': 'Internet',
            'LUZ': 'Energia',
            'ENERGIA': 'Energia',
            'SUPERMERCADO': 'Alimentação',
            'FOOD': 'Alimentação',
            'RESTAURANTE': 'Alimentação',
        }

        # Busca todas as contas do usuário para fazer o match
        user_accounts = Account.objects.filter(user_id=user_id)
        account_map = {acc.name.lower(): acc for acc in user_accounts}

        count = 0
        for trans in ofx.account.statement.transactions:
            # Tenta encontrar uma sugestão
            suggested_acc = None
            memo_upper = trans.memo.upper()
            
            for keyword, acc_name in KEYWORD_MAPPING.items():
                if keyword in memo_upper:
                    # Tenta achar a conta pelo nome sugerido
                    # O nome da conta deve bater com o valor do mapa
                    # Procura insensivel a caixa no mapa de contas do usuario
                    for u_acc_name, u_acc in account_map.items():
                        if acc_name.lower() in u_acc_name:
                            suggested_acc = u_acc
                            break
                if suggested_acc:
                    break
            
            # Cria o registro se não existir (baseado no fitid)
            if not BankReconciliation.objects.filter(fitid=trans.id, user_id=user_id).exists():
                BankReconciliation.objects.create(
                    user_id=user_id,
                    date=trans.date,
                    description=trans.memo,
                    amount=trans.amount,
                    fitid=trans.id,
                    suggested_account=suggested_acc,
                    status=BankReconciliation.STATUS_PENDING
                )
                count += 1
        
        print(f"[OFX] Processamento concluído. Novos registros: {count}")

    except Exception as e:
        import traceback
        print(f"[OFX] ERRO CRÍTICO no processamento: {str(e)}")
        print(traceback.format_exc())
    finally:
        # Limpa arquivo temporário
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"[OFX] Arquivo temporário removido.")
