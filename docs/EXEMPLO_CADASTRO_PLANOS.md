# Exemplo de Cadastro de Planos

## Como cadastrar planos via Django Admin

1. Acesse o admin em: `http://localhost:8000/admin/`
2. Navegue até **Services > Planos**
3. Clique em **Adicionar Plano**
4. Preencha os campos:
   - **Nome**: Bronze
   - **Categoria**: Serviços
   - **Preço**: 259.90
   - **Preço Antigo**: 329.90
   - **Descrição**: Perfeito para quem precisa de suporte, autonomia e agilidade no dia a dia.
   - **Features**: (JSON)
   - **Ativo**: ✓
   - **Destaque**: (deixe desmarcado)
   - **Ordem**: 1

## Exemplo de Features (JSON)

Para o campo **Features**, copie e cole este formato JSON:

```json
[
  "Contabilidade completa",
  "Certificado digital incluído",
  "Painel contábil",
  "Atendimento multicanal (8h-18h)",
  "Painel de RH (até 3 pessoas)",
  "Financeiro automático",
  "Importação até 50 notas fiscais",
  "Link de Pagamento",
  "Benefícios exclusivos"
]
```

## Cadastro Rápido via Shell do Django

Se preferir, você pode cadastrar os planos via linha de comando:

```bash
docker-compose exec web python manage.py shell
```

Depois, cole este código:

```python
from apps.services.models import Plano

# Plano Bronze - Serviços
Plano.objects.create(
    nome="Bronze",
    categoria="servicos",
    preco=259.90,
    preco_antigo=329.90,
    descricao="Perfeito para quem precisa de suporte, autonomia e agilidade no dia a dia.",
    features=[
        "Contabilidade completa",
        "Certificado digital incluído",
        "Painel contábil",
        "Atendimento multicanal (8h-18h)",
        "Painel de RH (até 3 pessoas)",
        "Financeiro automático",
        "Importação até 50 notas fiscais",
        "Link de Pagamento",
        "Benefícios exclusivos"
    ],
    ativo=True,
    destaque=False,
    ordem=1
)

# Plano Prata - Serviços (Mais Popular)
Plano.objects.create(
    nome="Prata",
    categoria="servicos",
    preco=349.90,
    preco_antigo=569.90,
    descricao="Tenha um gerente de conta dedicado para sua empresa.",
    features=[
        "Todos os benefícios do Bronze",
        "Gerente de conta exclusivo",
        "Painel de RH (até 5 pessoas)",
        "Importação em qualquer município",
        "IR para sócios",
        "Conciliação financeira",
        "Atendimento estendido (até 21h)",
        "Consultoria contábil",
        "Agendamento/emissão (até 40/mês)",
        "Importação até 100 notas",
        "Importação de extrato (até 2 contas)"
    ],
    ativo=True,
    destaque=True,  # Marca como "Mais Popular"
    ordem=2
)

# Plano Ouro - Serviços
Plano.objects.create(
    nome="Ouro",
    categoria="servicos",
    preco=699.90,
    preco_antigo=879.90,
    descricao="Para quem tem uma operação maior e mais demandas financeiras.",
    features=[
        "Todos os benefícios do Prata",
        "Painel de RH (até 10 pessoas)",
        "Agendamento/emissão (até 100/mês)",
        "Importação até 800 notas",
        "Importação de extrato (até 3 contas)"
    ],
    ativo=True,
    destaque=False,
    ordem=3
)

# Plano Bronze - Comércio
Plano.objects.create(
    nome="Bronze",
    categoria="comercio",
    preco=309.90,
    preco_antigo=379.90,
    descricao="Essencial para quem está começando a vender produtos e precisa de uma contabilidade organizada.",
    features=[
        "Contabilidade completa para comércio",
        "Cálculo de ICMS, PIS/COFINS",
        "Certificado digital incluído",
        "Painel contábil",
        "Atendimento multicanal (8h-18h)",
        "Painel de RH (até 3 pessoas)",
        "Controle de estoque básico",
        "Emissão de até 50 notas (NF-e)",
        "Link de Pagamento",
        "Benefícios exclusivos"
    ],
    ativo=True,
    destaque=False,
    ordem=1
)

# Plano Prata - Comércio (Mais Popular)
Plano.objects.create(
    nome="Prata",
    categoria="comercio",
    preco=399.90,
    preco_antigo=619.90,
    descricao="Ideal para lojas em crescimento que buscam mais controle financeiro e fiscal.",
    features=[
        "Todos os benefícios do Bronze",
        "Gerente de conta exclusivo",
        "Painel de RH (até 5 pessoas)",
        "Gestão de impostos (ICMS-ST)",
        "IR para sócios",
        "Conciliação financeira",
        "Atendimento estendido (até 21h)",
        "Emissão de até 150 notas (NF-e)",
        "Importação de extrato (até 2 contas)"
    ],
    ativo=True,
    destaque=True,
    ordem=2
)

# Plano Ouro - Comércio
Plano.objects.create(
    nome="Ouro",
    categoria="comercio",
    preco=749.90,
    preco_antigo=929.90,
    descricao="Para operações de e-commerce e varejo com alto volume e maior complexidade.",
    features=[
        "Todos os benefícios do Prata",
        "Painel de RH (até 10 pessoas)",
        "Planejamento tributário",
        "Emissão de até 900 notas (NF-e)",
        "Agendamento de pagamentos (até 100/mês)",
        "Importação de extrato (até 3 contas)"
    ],
    ativo=True,
    destaque=False,
    ordem=3
)

print("✅ 6 planos cadastrados com sucesso!")
print(f"Total de planos: {Plano.objects.count()}")
```

## Planos para Abertura de Empresa

Se quiser criar planos específicos para a abertura de empresas (usados na etapa 9 do wizard):

```python
# Plano de Abertura MEI
Plano.objects.create(
    nome="Abertura MEI",
    categoria="abertura",
    preco=149.90,
    descricao="Abertura completa de MEI com toda documentação.",
    features=[
        "Registro no CNPJ",
        "Alvará automático",
        "Suporte via WhatsApp",
        "Entrega em até 3 dias úteis"
    ],
    mercadopago_price_id="",  # Adicione o ID do Mercado Pago depois
    ativo=True,
    ordem=1
)

# Plano de Abertura ME/LTDA
Plano.objects.create(
    nome="Abertura ME/LTDA",
    categoria="abertura",
    preco=499.90,
    preco_antigo=799.90,
    descricao="Abertura completa de ME ou LTDA com contrato social.",
    features=[
        "Registro na Junta Comercial",
        "Registro no CNPJ",
        "Contrato Social incluso",
        "Alvará de funcionamento",
        "Inscrição Municipal/Estadual",
        "Suporte especializado",
        "Entrega em até 10 dias úteis"
    ],
    mercadopago_price_id="",
    ativo=True,
    destaque=True,
    ordem=2
)

print("✅ Planos de abertura cadastrados!")
```

## Integração com Mercado Pago

Para integrar com o Mercado Pago, siga estes passos:

1. Crie os produtos/preços no painel do Mercado Pago
2. Copie o `price_id` ou `product_id` de cada plano
3. Edite cada plano no admin e cole o ID no campo **Mercadopago Price Id**

Exemplo:
```
mercadopago_price_id: "price_1234567890abcdef"
```

## Verificando os Planos na Homepage

Após cadastrar os planos, acesse:
- `http://localhost:8000/` - Planos aparecerão automaticamente
- Use o toggle "Serviços/Comércio" para alternar entre categorias

## Campos do Modelo Plano

| Campo | Tipo | Descrição |
|-------|------|-----------|
| nome | CharField | Nome do plano (ex: Bronze, Prata, Ouro) |
| categoria | CharField | Categoria: servicos, comercio ou abertura |
| preco | DecimalField | Preço atual do plano |
| preco_antigo | DecimalField | Preço anterior (para mostrar desconto) |
| descricao | TextField | Descrição curta do plano |
| features | JSONField | Lista JSON com características |
| mercadopago_price_id | CharField | ID do produto no Mercado Pago |
| ativo | BooleanField | Se o plano está ativo |
| destaque | BooleanField | Marca como "Mais Popular" |
| ordem | IntegerField | Ordem de exibição |

## Métodos Úteis do Modelo

```python
plano = Plano.objects.first()

# Verifica se tem desconto
plano.tem_desconto()  # True/False

# Calcula percentual de desconto
plano.percentual_desconto()  # Ex: 21.0 (21%)

# String representation
str(plano)  # "Bronze - Serviços (R$ 259.90)"
```
