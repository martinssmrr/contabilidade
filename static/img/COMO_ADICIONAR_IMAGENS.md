# 🖼️ Guia Rápido: Como Adicionar as Imagens

## Opção 1: Criar Imagens Placeholder Temporárias

Se você não tem as imagens ainda, pode usar placeholders temporários:

### Usando um gerador online:

1. **Para logo.png**:
   - Acesse: https://via.placeholder.com/300x80/1e3a8a/ffffff?text=Gestão+360
   - Clique com botão direito → Salvar imagem como
   - Salve como `logo.png` na pasta `static/img/`

2. **Para popup_home.png**:
   - Acesse: https://via.placeholder.com/600x800/06b6d4/ffffff?text=Contabilidade+Online
   - Clique com botão direito → Salvar imagem como
   - Salve como `popup_home.png` na pasta `static/img/`

---

## Opção 2: Usar Canva ou Photoshop

### Logo (logo.png)

**Especificações**:
- Dimensões: 300x80 pixels
- Formato: PNG com fundo transparente
- Cores: Use as cores do projeto
  - Azul marinho: #1e3a8a
  - Ciano: #06b6d4
  - Âmbar: #f59e0b

**Sugestões de Design**:
- Texto "Gestão 360" em fonte moderna (Inter, Montserrat, Poppins)
- Ícone de gráfico ou calculadora ao lado
- Gradiente das cores primárias

### Imagem do Popup (popup_home.png)

**Especificações**:
- Dimensões: 600x800 pixels (vertical)
- Formato: PNG ou JPG
- Estilo: Moderno, profissional, minimalista

**Sugestões de Conteúdo**:
- Pessoa trabalhando em laptop
- Gráficos ou relatórios de negócios
- Ambiente de escritório moderno
- Ilustração de contabilidade digital

**Sites para encontrar imagens gratuitas**:
- Unsplash: https://unsplash.com
- Pexels: https://pexels.com
- Freepik: https://freepik.com (alguns gratuitos)

---

## Opção 3: Usar IA para Gerar Imagens

### Para o Popup (DALL-E, Midjourney, etc.)

**Prompt sugerido**:
```
"Modern professional accountant working on laptop in bright office, 
blue and teal color scheme, minimalist style, vertical composition, 
high quality, corporate photography"
```

ou

```
"Ilustração vetorial moderna de contabilidade digital, 
cores azul marinho e ciano, estilo minimalista e profissional, 
gráficos e documentos, vertical"
```

---

## 📂 Onde Colocar as Imagens

```
gestao360/
└── static/
    └── img/
        ├── logo.png          ← Logo da empresa
        ├── popup_home.png    ← Imagem do popup
        └── README.md         ← Instruções
```

---

## 🔄 Depois de Adicionar as Imagens

### 1. Se estiver usando Docker:

```powershell
# Copiar arquivos para o container
docker cp static/img/logo.png gestao360_web:/app/static/img/
docker cp static/img/popup_home.png gestao360_web:/app/static/img/

# Executar collectstatic
docker-compose exec web python manage.py collectstatic --noinput
```

### 2. Se estiver rodando local (sem Docker):

```powershell
# Apenas execute collectstatic
python manage.py collectstatic --noinput
```

### 3. Limpar cache do navegador

- **Chrome/Edge**: Ctrl + Shift + Delete → Limpar imagens e arquivos em cache
- **Firefox**: Ctrl + Shift + Delete → Cache
- Ou use modo anônimo/privado (Ctrl + Shift + N)

### 4. Recarregar a página

- Pressione `Ctrl + F5` (recarregamento forçado)
- Ou `F5` para recarregar normal

---

## ✅ Verificar se Funcionou

1. Abra o site: http://localhost:8000
2. A logo deve aparecer:
   - No topo da navbar (esquerda)
   - No centro do hero section (grande)
3. O popup deve abrir após 2 segundos
4. A imagem deve aparecer no lado esquerdo do popup

---

## ⚠️ Problemas Comuns

### Logo não aparece
- Verifique o nome do arquivo: deve ser exatamente `logo.png`
- Verifique o caminho: `static/img/logo.png`
- Execute collectstatic novamente
- Limpe o cache do navegador

### Imagem do popup não aparece
- Verifique o nome: deve ser exatamente `popup_home.png`
- Verifique o caminho: `static/img/popup_home.png`
- Verifique o console do navegador (F12) para erros 404
- Se ver erro 404, o caminho está errado

### Imagens aparecem distorcidas
- Logo: redimensione para aproximadamente 300x80px
- Popup: redimensione para aproximadamente 600x800px
- Mantenha a proporção (aspect ratio)

---

## 🎨 Dicas de Design

### Cores do Projeto
Use estas cores nas suas imagens para manter consistência:

- **Primária**: #1e3a8a (Azul Marinho)
- **Secundária**: #06b6d4 (Ciano)
- **Destaque**: #f59e0b (Âmbar/Dourado)

### Fontes Recomendadas
- Inter (atual do site)
- Montserrat
- Poppins
- Roboto

### Estilo Visual
- Minimalista e limpo
- Moderno e profissional
- Cores vibrantes mas não exageradas
- Gradientes sutis

---

## 📱 Testar Responsividade

Depois de adicionar as imagens, teste em diferentes tamanhos:

1. Pressione `F12` no navegador
2. Clique no ícone de dispositivo móvel (ou Ctrl + Shift + M)
3. Teste em:
   - iPhone SE (375px)
   - iPhone 12 Pro (390px)
   - iPad (768px)
   - Desktop (1920px)

---

## 🚀 URLs Úteis para Download de Imagens

### Imagens Gratuitas de Alta Qualidade
- https://unsplash.com/s/photos/accounting
- https://pexels.com/search/business/
- https://pixabay.com/images/search/office/

### Ícones e Ilustrações
- https://undraw.co/illustrations
- https://icons8.com/illustrations
- https://storyset.com/

### Ferramentas de Edição Online
- https://www.canva.com/
- https://www.photopea.com/ (Photoshop online)
- https://www.remove.bg/ (remover fundo)

---

**Precisa de ajuda?** Consulte o arquivo `docs/ATUALIZACAO_DESIGN.md` para mais detalhes!
