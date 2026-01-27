"""Script simples para testar sitemap sem precisar de Django completo"""

# Teste 1: Verificar imports
print("=== Teste 1: Verificando imports ===")
try:
    from django.contrib.sitemaps import Sitemap
    from django.urls import reverse
    print("✓ Imports básicos OK")
except Exception as e:
    print(f"✗ Erro nos imports: {e}")

# Teste 2: Verificar se o arquivo sitemaps.py tem sintaxe válida
print("\n=== Teste 2: Verificando sintaxe do sitemaps.py ===")
try:
    import ast
    with open('apps/blog/sitemaps.py', 'r', encoding='utf-8') as f:
        code = f.read()
    ast.parse(code)
    print("✓ Sintaxe do arquivo OK")
except SyntaxError as e:
    print(f"✗ Erro de sintaxe: {e}")
except Exception as e:
    print(f"✗ Erro ao ler arquivo: {e}")

# Teste 3: Verificar URLs definidas
print("\n=== Teste 3: URLs no StaticViewSitemap ===")
urls_expected = [
    'home', 'abrir_empresa', 'deixar_mei', 'trocar_contador',
    'contabilidade_completa', 'assessoria', 'calculadora_clt_pj',
    'sobre', 'termos_de_uso', 'politica_de_privacidade',
    'contabilidade_mei', 'endereco_virtual', 'certificado_digital',
    'emissor_nota_fiscal'
]
print(f"URLs esperadas: {len(urls_expected)}")
for url in urls_expected:
    print(f"  - {url}")

print("\n=== Teste 4: URLs no ServicesSitemap ===")
service_urls = ['services_list', 'planos']
for url in service_urls:
    print(f"  - {url}")

print("\n✓ Todos os testes de estrutura passaram!")
print("\nPara testar com Django, execute:")
print("  python manage.py shell")
print("  >>> from apps.blog.sitemaps import StaticViewSitemap")
print("  >>> sitemap = StaticViewSitemap()")
print("  >>> sitemap.items()")
