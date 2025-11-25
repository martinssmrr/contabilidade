# Guia: Google Search Console - Vetorial Contabilidade

## 📋 Checklist de Arquivos Criados

✅ **robots.txt** - Instrui crawlers do Google sobre páginas permitidas/bloqueadas
✅ **sitemap.xml** - Mapa do site gerado dinamicamente com todas as páginas
✅ **sitemaps.py** - Gerador de sitemaps para páginas estáticas, blog, serviços e planos
✅ **schema_org.json** - Dados estruturados para Rich Snippets do Google
✅ **Meta tags SEO** - Open Graph, Twitter Cards, canonical, robots

---

## 🚀 Passos para Publicar no Google Search Console

### 1. Acesse o Google Search Console
- URL: https://search.google.com/search-console
- Faça login com sua conta Google

### 2. Adicione a Propriedade
- Clique em "Adicionar propriedade"
- Escolha **Prefixo do URL**: `https://contabilvetorial.com.br`

### 3. Verificação de Propriedade (Escolha um método)

#### **Opção A: Tag HTML (Recomendado)**
1. O Google vai fornecer uma meta tag como:
   ```html
   <meta name="google-site-verification" content="CÓDIGO_AQUI" />
   ```
2. Adicione essa tag no `templates/base.html` dentro do `<head>`
3. Faça deploy e clique em "Verificar"

#### **Opção B: Arquivo HTML**
1. Baixe o arquivo HTML fornecido pelo Google (ex: `google1234567890abcdef.html`)
2. Coloque em `templates/google1234567890abcdef.html`
3. Adicione rota em `urls.py`:
   ```python
   path('google1234567890abcdef.html', TemplateView.as_view(template_name='google1234567890abcdef.html')),
   ```
4. Faça deploy e clique em "Verificar"

#### **Opção C: DNS (Requer acesso ao painel de domínio)**
1. Adicione registro TXT no DNS do domínio com o código fornecido
2. Aguarde propagação (pode levar algumas horas)
3. Clique em "Verificar"

### 4. Envie o Sitemap
Após verificação:
1. Vá em **Sitemaps** no menu lateral
2. Digite: `sitemap.xml`
3. Clique em "Enviar"

### 5. Configure o robots.txt
- Acesse: `https://contabilvetorial.com.br/robots.txt`
- Verifique se está acessível
- O Search Console testará automaticamente

---

## 🔍 URLs Importantes do Site

**Páginas principais:**
- Home: https://contabilvetorial.com.br/
- Abrir Empresa: https://contabilvetorial.com.br/abrir-empresa/
- Serviços: https://contabilvetorial.com.br/services/planos/
- Blog: https://contabilvetorial.com.br/blog/
- Calculadora: https://contabilvetorial.com.br/recursos/calculadora-clt-pj/

**SEO:**
- Sitemap: https://contabilvetorial.com.br/sitemap.xml
- Robots: https://contabilvetorial.com.br/robots.txt

---

## 📊 Monitoramento Pós-Publicação

### Métricas para Acompanhar:
1. **Cobertura** - Páginas indexadas vs. excluídas
2. **Desempenho** - Cliques, impressões, CTR, posição média
3. **Experiência** - Core Web Vitals (LCP, FID, CLS)
4. **Usabilidade móvel** - Problemas em dispositivos móveis
5. **Links** - Backlinks externos e links internos

### Tarefas Recorrentes:
- [ ] Enviar sitemap após adicionar novos posts no blog
- [ ] Monitorar erros de rastreamento semanalmente
- [ ] Solicitar re-indexação de páginas importantes após mudanças
- [ ] Acompanhar palavras-chave e melhorar conteúdo

---

## 🎯 Otimizações Aplicadas

### 1. **Meta Tags**
- Title otimizado (50-60 caracteres)
- Description atrativa (150-160 caracteres)
- Keywords relevantes
- Robots: index, follow
- Canonical URLs

### 2. **Open Graph** (Facebook)
- og:type, og:url, og:title, og:description, og:image
- Melhora compartilhamento em redes sociais

### 3. **Twitter Cards**
- Imagens e descrições otimizadas para Twitter

### 4. **Schema.org**
- Tipo: Organization
- Dados estruturados para Rich Snippets
- Nome, logo, descrição, endereço, contato

### 5. **Sitemap XML**
- Geração automática de URLs
- Prioridades e frequências de atualização
- Separado por tipo: estáticas, blog, serviços

### 6. **Robots.txt**
- Permite crawlers em páginas públicas
- Bloqueia admin, dashboard, uploads
- Referencia sitemap.xml

---

## 🛠️ Comandos de Deploy

```bash
# Local - verificar sitemap
curl http://localhost:8000/sitemap.xml

# Produção - após deploy
ssh root@contabilvetorial.com.br
cd /root/vetorial
git pull
docker-compose -f docker-compose.prod.yml restart web

# Testar em produção
curl https://contabilvetorial.com.br/sitemap.xml
curl https://contabilvetorial.com.br/robots.txt
```

---

## ✅ Próximos Passos

1. **Agora:**
   - [ ] Fazer commit e push das alterações
   - [ ] Deploy em produção
   - [ ] Verificar sitemap.xml e robots.txt acessíveis
   - [ ] Adicionar propriedade no Google Search Console
   - [ ] Verificar propriedade (escolher método)
   - [ ] Enviar sitemap

2. **Em 24-48 horas:**
   - [ ] Verificar páginas indexadas
   - [ ] Corrigir erros de rastreamento (se houver)

3. **Semanalmente:**
   - [ ] Monitorar desempenho e impressões
   - [ ] Publicar novos posts no blog
   - [ ] Atualizar sitemap (automático)

4. **Mensalmente:**
   - [ ] Analisar palavras-chave
   - [ ] Otimizar conteúdo com baixo CTR
   - [ ] Verificar Core Web Vitals

---

## 📞 Dúvidas Comuns

**Q: Quanto tempo leva para aparecer no Google?**
A: De 1 a 7 dias após verificação e envio do sitemap.

**Q: Por que minha página não está indexada?**
A: Verifique em Cobertura > Excluídas. Pode ser robots.txt, meta robots=noindex, ou conteúdo duplicado.

**Q: Como solicitar indexação rápida?**
A: Use a ferramenta "Inspeção de URL" e clique em "Solicitar indexação".

**Q: Preciso fazer algo após publicar novo post?**
A: Não, o sitemap é atualizado automaticamente. Mas pode solicitar re-indexação manual para acelerar.
