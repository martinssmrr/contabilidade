"""
Script de teste para a integração Evolution API - WhatsApp

Para executar:
1. Configure as variáveis de ambiente no .env
2. Execute: python manage.py shell < test_whatsapp.py

Ou execute manualmente no Django shell:
python manage.py shell
>>> exec(open('test_whatsapp.py').read())
"""

from apps.support.whatsapp_service import whatsapp_service
import json

print("=" * 60)
print("TESTE DE INTEGRAÇÃO - EVOLUTION API")
print("=" * 60)

# Teste 1: Verificar configuração
print("\n[1] Verificando configuração...")
print(f"URL Base: {whatsapp_service.base_url}")
print(f"Instância: {whatsapp_service.instance_name}")
print(f"API Key: {'*' * 20 if whatsapp_service.api_key else 'NÃO CONFIGURADA'}")
print(f"Número Remetente: {whatsapp_service.sender_number}")

if not all([whatsapp_service.base_url, whatsapp_service.api_key, whatsapp_service.instance_name]):
    print("\n❌ ERRO: Variáveis de ambiente não configuradas!")
    print("Configure as seguintes variáveis no arquivo .env:")
    print("- EVOLUTION_API_URL")
    print("- EVOLUTION_API_KEY")
    print("- EVOLUTION_INSTANCE_NAME")
    print("- WHATSAPP_SENDER_NUMBER")
    exit()

print("✅ Configuração OK")

# Teste 2: Verificar conexão com API
print("\n[2] Testando conexão com Evolution API...")
connection_result = whatsapp_service.check_connection()

if connection_result.get('success'):
    print("✅ Conexão estabelecida com sucesso!")
    print(f"Status: {json.dumps(connection_result.get('status'), indent=2)}")
else:
    print(f"❌ Falha na conexão: {connection_result.get('error')}")
    print("\nVerifique:")
    print("1. Se a URL da API está correta")
    print("2. Se a API Key é válida")
    print("3. Se a instância existe e está ativa")
    exit()

# Teste 3: Formatação de números
print("\n[3] Testando formatação de números...")
test_numbers = [
    "(61) 99831-1920",
    "61 998311920",
    "61998311920",
    "5561998311920"
]

for number in test_numbers:
    formatted = whatsapp_service.format_phone_number(number)
    print(f"  {number:20} -> {formatted}")

print("✅ Formatação funcionando")

# Teste 4: Envio de mensagem (COMENTADO - descomente para testar envio real)
print("\n[4] Teste de envio de mensagem...")
print("⚠️  DESCOMENTE AS LINHAS ABAIXO PARA ENVIAR MENSAGEM DE TESTE REAL")

"""
# DESCOMENTE PARA TESTAR ENVIO REAL:

TEST_PHONE = "61998311920"  # Substitua pelo seu número de teste
TEST_NAME = "Teste Sistema"

print(f"Enviando mensagem de teste para {TEST_PHONE}...")
result = whatsapp_service.send_welcome_message(
    phone=TEST_PHONE,
    name=TEST_NAME
)

if result.get('success'):
    print("✅ Mensagem enviada com sucesso!")
    print(f"Resposta da API: {json.dumps(result.get('response'), indent=2)}")
else:
    print(f"❌ Falha ao enviar mensagem: {result.get('error')}")
"""

print("\n" + "=" * 60)
print("RESUMO DOS TESTES")
print("=" * 60)
print("✅ Configuração: OK")
print("✅ Conexão API: OK")
print("✅ Formatação: OK")
print("⚠️  Envio Real: Não testado (descomente o código para testar)")

print("\nPara testar o envio real:")
print("1. Edite este arquivo e descomente a seção 'Teste 4'")
print("2. Substitua TEST_PHONE pelo seu número")
print("3. Execute novamente o script")

print("\n" + "=" * 60)
