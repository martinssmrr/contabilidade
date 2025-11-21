# Atualização de Design - Gestão 360

## 📋 Resumo das Alterações

### Data: 2024
**Objetivo**: Modernizar o design do sistema com base nas cores da logo e adicionar popup de contato interativo

---

## 🎨 Design Atualizado

### Esquema de Cores
As cores foram baseadas na logo do projeto:

- **Primária**: `#1e3a8a` (Azul Marinho)
- **Primária Escura**: `#1e40af` 
- **Primária Clara**: `#3b82f6`
- **Secundária**: `#06b6d4` (Ciano)
- **Destaque**: `#f59e0b` (Âmbar/Dourado)
- **Sucesso**: `#10b981` (Verde)
- **Erro**: `#ef4444` (Vermelho)

### Elementos Visuais Atualizados

#### 1. Hero Section
- Gradiente moderno usando cores primárias
- Logo centralizada com filtro de inversão para contraste
- Animação de fade-in ao carregar
- Radial gradient overlay para profundidade

#### 2. Navbar
- Gradiente de fundo (primária → primária escura)
- Logo com filtro de inversão branca
- Animação de underline nos links ao hover
- Sombra suave para profundidade

#### 3. Cards
- Border-radius arredondado (16px)
- Animação de elevação ao hover
- Sombra moderna com cor primária
- Transição suave com cubic-bezier

#### 4. Botões
- Efeito ripple ao clicar
- Gradientes para diferentes tipos
- Animação de elevação ao hover
- Bordas arredondadas (12px)

#### 5. Stats Section
- Números em cor primária
- Tipografia grande e impactante
- Responsivo para mobile

---

## 🔔 Popup de Contato

### Características
- **Layout**: Duas colunas (imagem + formulário)
- **Ativação**: Automática após 2 segundos
- **Controle**: SessionStorage para não repetir na mesma sessão
- **Responsivo**: Stack vertical em mobile

### Campos do Formulário
1. Nome Completo (obrigatório)
2. E-mail (obrigatório, com validação)
3. Telefone (obrigatório, com máscara automática)
4. Estado (dropdown com todos os estados brasileiros)
5. Cidade (obrigatório)
6. Serviço desejado (dropdown):
   - Abrir uma empresa
   - Trocar de contador
   - Mudar de MEI para ME
   - Contabilidade para MEI
   - Abrir MEI

### Funcionalidades
- **Botão WhatsApp**: Abre conversa com mensagem pré-preenchida
- **Botão Ligação**: Exibe confirmação e fecha modal
- **Validação**: Campos obrigatórios e formato de email
- **Máscara**: Telefone no formato (00) 00000-0000

---

## 📁 Arquivos Modificados

### 1. `templates/home.html`
**Mudanças**:
- Adicionado modal popup de contato no topo
- Removidos estilos inline
- Adicionado bloco `extra_js` com JavaScript do popup
- Hero section com nova estrutura
- Smooth scroll para links internos

### 2. `static/css/style.css`
**Mudanças**:
- Adicionadas variáveis CSS com novo esquema de cores
- Estilos para hero section com gradiente
- Estilos para CTA section
- Estilos para stats section
- Estilos completos do popup/modal
- Classes utilitárias (animate-fade-in, stats-number, hero-logo)
- Responsividade para mobile

### 3. `templates/base.html`
**Status**: Sem alterações (já continha bloco extra_js)

### 4. `static/img/README.md` (NOVO)
**Conteúdo**: Instruções para adicionar as imagens necessárias

---

## 🖼️ Imagens Necessárias

### Logo (logo.png)
- **Local**: `static/img/logo.png`
- **Uso**: Navbar e Hero Section
- **Dimensões recomendadas**: 300x80px
- **Formato**: PNG com fundo transparente
- **Cores**: Deve conter azul marinho, ciano e âmbar

### Imagem do Popup (popup_home.png)
- **Local**: `static/img/popup_home.png`
- **Uso**: Lado esquerdo do modal de contato
- **Dimensões recomendadas**: 600x800px (vertical)
- **Formato**: PNG ou JPG
- **Sugestão**: Imagem relacionada a contabilidade/atendimento

---

## 🚀 Como Testar

### 1. Certifique-se de que o Docker está rodando
```powershell
docker-compose ps
```

### 2. Se não estiver rodando, inicie os containers
```powershell
docker-compose up -d
```

### 3. Acesse o site
```
http://localhost:8000
```

### 4. O popup deve aparecer automaticamente após 2 segundos

### 5. Teste as funcionalidades
- Preencha o formulário
- Teste o botão WhatsApp
- Teste o botão de Ligação
- Verifique a responsividade (F12 → dispositivos móveis)
- Recarregue a página (F5) - popup NÃO deve aparecer na mesma sessão
- Abra em nova aba/janela anônima - popup deve aparecer novamente

---

## 📱 Responsividade

### Breakpoints
- **Desktop**: > 768px (layout de 2 colunas no popup)
- **Mobile**: ≤ 768px (layout empilhado no popup)

### Ajustes Mobile
- Popup vira stack vertical
- Imagem do popup com altura reduzida (250px)
- Padding reduzido no formulário
- Botões com tamanho menor
- Stats com fonte reduzida

---

## 🔧 Próximos Passos

### Backend
1. Criar view Django para processar o formulário de contato
2. Configurar envio de email com os dados do formulário
3. Adicionar modelo no banco para salvar leads
4. Implementar integração com CRM (opcional)

### Frontend
5. Adicionar mais animações (AOS, GSAP)
6. Implementar lazy loading de imagens
7. Otimizar performance (minimizar CSS/JS)
8. Adicionar página de serviços detalhada
9. Criar dashboard diferenciado para cada tipo de usuário

### Integrações
10. Configurar API do WhatsApp Business
11. Integrar com Mercado Pago para pagamentos
12. Implementar chat ao vivo (Tawk.to, Zendesk)
13. Google Analytics e Google Tag Manager

---

## 📞 Configurações Importantes

### Número do WhatsApp
**Arquivo**: `templates/home.html` (linha ~307)
```javascript
const whatsappNumber = '5511999999999'; // ALTERE AQUI
```
**Formato**: Código do país (55) + DDD + número (sem espaços ou caracteres especiais)

### Email de Contato
Atualmente o formulário apenas exibe um alert. Para implementar envio real:

1. Criar view em `apps/support/views.py`
2. Adicionar URL em `urls.py`
3. Configurar SMTP em `settings.py`
4. Atualizar JavaScript para fazer POST via fetch()

---

## 🎯 Melhorias de UX Implementadas

1. **Feedback Visual**: Hover states em todos os elementos clicáveis
2. **Validação em Tempo Real**: Máscaras e validações de campos
3. **Smooth Scroll**: Navegação suave para links internos
4. **Loading States**: Transições suaves entre estados
5. **Acessibilidade**: Labels, aria-labels e contraste adequado
6. **Mobile-First**: Design responsivo e touch-friendly

---

## ⚠️ Avisos de Lint

Os avisos de "inline styles" que aparecem são apenas alertas de boas práticas.
Todos os estilos inline foram movidos para o arquivo CSS, usando classes específicas:

- `.hero-section` - Gradiente do hero
- `.cta-section` - Gradiente da CTA
- `.stats-number` - Cor dos números de estatística
- `.hero-logo` - Logo no hero section
- `.popup-image` - Imagem de fundo do popup

---

## 📚 Recursos Utilizados

- **Bootstrap 5.3**: Framework CSS
- **Bootstrap Icons**: Ícones SVG
- **Google Fonts**: Inter (fonte moderna)
- **JavaScript Vanilla**: Sem dependências externas
- **CSS Variables**: Para fácil customização de cores
- **CSS Grid/Flexbox**: Layout responsivo

---

## ✅ Checklist de Implementação

- [x] Atualizar esquema de cores baseado na logo
- [x] Criar popup de contato
- [x] Adicionar formulário com validações
- [x] Implementar botões WhatsApp e Ligação
- [x] Adicionar máscara de telefone
- [x] Tornar design responsivo
- [x] Mover estilos inline para CSS
- [x] Adicionar animações modernas
- [x] Implementar smooth scroll
- [x] Criar documentação
- [ ] Adicionar imagens (logo.png, popup_home.png)
- [ ] Configurar número real do WhatsApp
- [ ] Criar backend para processar formulário
- [ ] Testar em diferentes navegadores
- [ ] Otimizar performance

---

**Desenvolvido com ❤️ para Gestão 360**
