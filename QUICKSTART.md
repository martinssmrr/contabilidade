# ==================================
# SCRIPT DE INICIALIZAÇÃO RÁPIDA
# ==================================
# Este script configura o ambiente de desenvolvimento rapidamente

# GUIA DE INÍCIO RÁPIDO - GESTÃO 360

## 1. PRIMEIRA VEZ? SIGA ESTES PASSOS:

### Windows (PowerShell):
```powershell
# 1. Criar ambiente virtual
python -m venv venv
.\venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Copiar arquivo de ambiente
cp .env.example .env

# 4. Editar .env com suas credenciais (usar notepad ou VSCode)
notepad .env

# 5. Executar migrações
python manage.py makemigrations
python manage.py migrate

# 6. Criar superusuário
python manage.py createsuperuser

# 7. Iniciar servidor
python manage.py runserver
```

### Linux/Mac (Bash):
```bash
# 1. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Copiar arquivo de ambiente
cp .env.example .env

# 4. Editar .env com suas credenciais
nano .env

# 5. Executar migrações
python manage.py makemigrations
python manage.py migrate

# 6. Criar superusuário
python manage.py createsuperuser

# 7. Iniciar servidor
python manage.py runserver
```

## 2. USANDO DOCKER (RECOMENDADO):

```bash
# 1. Copiar arquivo de ambiente
cp .env.example .env

# 2. Editar .env (importante!)
# Definir credenciais do PostgreSQL

# 3. Iniciar containers
docker-compose up -d

# 4. Executar migrações
docker-compose exec web python manage.py migrate

# 5. Criar superusuário
docker-compose exec web python manage.py createsuperuser

# 6. Acessar
# http://localhost:8000
```

## 3. CREDENCIAIS DO MERCADO PAGO:

1. Acesse: https://www.mercadopago.com.br/developers
2. Crie uma aplicação
3. Copie as credenciais de teste/produção
4. Cole no arquivo .env:
   - MP_PUBLIC_KEY
   - MP_ACCESS_TOKEN

## 4. ACESSAR O SISTEMA:

- **Frontend:** http://localhost:8000
- **Admin:** http://localhost:8000/admin
- **API:** http://localhost:8000/api (futuro)

## 5. COMANDOS ÚTEIS:

```bash
# Criar novo app
python manage.py startapp nome_do_app

# Fazer migrações
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Iniciar shell interativo
python manage.py shell

# Executar testes
python manage.py test
```

## 6. ESTRUTURA DE USUÁRIOS:

### Roles disponíveis:
- **cliente**: Acessa serviços, documentos e suporte
- **contador**: Gerencia clientes, cria documentos
- **admin**: Acesso total ao sistema
- **suporte**: Gerencia tickets de suporte

## 7. PRÓXIMOS PASSOS:

1. Personalizar templates em `templates/`
2. Adicionar estilos em `static/css/`
3. Criar views em cada app
4. Configurar URLs
5. Implementar lógica de pagamentos
6. Testar integração com Mercado Pago

## 8. TROUBLESHOOTING:

### Erro de conexão com PostgreSQL:
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no .env
- Para Docker: `docker-compose logs db`

### Erro de importação:
- Ative o ambiente virtual
- Reinstale: `pip install -r requirements.txt`

### Erro de migração:
- Delete arquivos em `*/migrations/` (exceto __init__.py)
- Recrie: `python manage.py makemigrations`
- Aplique: `python manage.py migrate`

## 9. DESENVOLVIMENTO:

Para desenvolver, recomendamos:
- VSCode com extensões Python e Django
- PostgreSQL rodando localmente ou via Docker
- Usar DEBUG=True apenas em desenvolvimento
- Testar pagamentos no ambiente de teste do Mercado Pago

---

🎉 **Parabéns! Seu projeto Gestão 360 está pronto para desenvolvimento!**
