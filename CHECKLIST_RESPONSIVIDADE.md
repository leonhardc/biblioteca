# ✅ Checklist de Responsividade - Guia do Desenvolvedor

## 🎯 Antes de Começar um Novo Template

- [x] Incluir `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- [x] Importar os 3 arquivos CSS responsivos
- [x] Usar classes grid (`row`, `col-*`) ou `display: grid`
- [ ] Começar com mobile-first approach
- [x] Pensar em como layout será em diferentes tamanhos

## 📝 Durante a Desenvolvimento

### Layout
- [ ] Define a estrutura mobile primeiro (xs: 320px)
- [ ] Adiciona quebras em sm (576px)
- [ ] Ajusta para md (768px)
- [ ] Otimiza para lg (992px)
- [ ] Aprova em xl (1200px+)

### Typography
- [ ] Títulos são legíveis em mobile?
- [ ] Tamanho de fonte adequado (14px min)
- [ ] Line height apropriado (1.4-1.6)
- [ ] Contrast satisfatório (WCAG AA)
- [ ] Usa unidades relativas (rem, em)

### Espaçamento
- [ ] Padding reduzido em mobile (1rem)
- [ ] Gap entre elementos (0.5rem - 1rem)
- [ ] Margin-bottom em elementos (1rem)
- [ ] Margem externa (1rem - 3rem por breakpoint)

### Componentes
- [ ] Botões têm min-height de 44px (touch-friendly)
- [ ] Inputs têm width: 100% em mobile
- [ ] Cards em grid responsivo
- [ ] Imagens com max-width: 100%
- [ ] Formulários single-column em mobile

### Formulários
- [ ] Campos full-width em mobile
- [ ] Labels acima dos inputs
- [ ] Espaçamento adequado entre campos
- [ ] Botões full-width em mobile
- [ ] Validação visível e clara

### Imagens e Mídia
- [ ] Imagens responsivas (max-width: 100%)
- [ ] Aspect ratio mantido
- [ ] Formato otimizado por dispositivo
- [ ] Lazy loading considerado
- [ ] Alt text em todas as imagens

### Navegação
- [ ] Menu hamburger em mobile
- [ ] Links com tamanho toque (44px)
- [ ] Breadcrumb responsivo
- [ ] Paginação responsiva
- [ ] Ativa em mobile de fácil acesso

### Viewport Responsivo
- [ ] Testar em 320px (iPhone SE)
- [ ] Testar em 375px (iPhone)
- [ ] Testar em 576px (landscape)
- [ ] Testar em 768px (tablet)
- [ ] Testar em 992px (laptop)
- [ ] Testar em 1920px (desktop)

## 🧪 Testes de Responsividade

### DevTools (Chrome/Firefox)
- [ ] Abrir DevTools (F12)
- [ ] Toggle Device Toolbar (Ctrl+Shift+M)
- [ ] Testar em dispositivos pré-definidos
- [ ] Testar em tamanhos customizados
- [ ] Orientação portrait e landscape
- [ ] Zoom até 200% (acessibilidade)

### Dispositivos Reais
- [ ] iPhone (375px - portrait)
- [ ] iPhone (812px - landscape)
- [ ] Android (360px - portrait)
- [ ] iPad (768px - portrait)
- [ ] iPad (1024px - landscape)
- [ ] Desktop (1920px+)

### Performance
- [ ] Lighthouse > 90
- [ ] Tempo de carregamento < 3s
- [ ] CSS minificado
- [ ] Sem CSS redundante
- [ ] Imagens otimizadas

### Acessibilidade
- [ ] Teclado navegável (Tab)
- [ ] Screen reader funciona
- [ ] Contraste adequado (WCAG AA)
- [ ] Sem imagens-texto
- [ ] Focus visível
- [ ] ARIA labels onde necessário

## 🎨 Implementação CSS Responsiva

### Classes Disponíveis

#### Display
```html
<!-- Usar para mostrar/esconder por breakpoint -->
d-none         <!-- Hidden -->
d-block        <!-- Display block -->
d-flex         <!-- Flexbox -->
d-grid         <!-- CSS Grid -->
d-xs / d-sm / d-md / d-lg / d-xl <!-- Por breakpoint -->
```

#### Grid
```html
<!-- Sistema de 12 colunas -->
<div class="row">
  <div class="col-12">Full width</div>
  <div class="col-6 col-md-4">6 cols mobile, 4 desktop</div>
</div>
```

#### Flexbox
```html
<!-- Utilities flexbox -->
d-flex              <!-- Display flex -->
flex-column         <!-- Column direction -->
flex-row            <!-- Row direction -->
justify-content-*   <!-- Justify content -->
align-items-*       <!-- Align items -->
gap-*               <!-- Gap between items -->
```

#### Spacing
```html
<!-- Margin -->
m-1, m-2, m-3, m-4, m-5    <!-- All sides -->
mt-*, mb-*, mx-*, my-*      <!-- Specific sides -->
mx-auto                      <!-- Center horizontally -->

<!-- Padding -->
p-1, p-2, p-3, p-4, p-5    <!-- All sides -->
px-*, py-*                   <!-- Specific sides -->
```

#### Tipografia
```html
h1, h2, h3, h4, h5, h6      <!-- Headings responsivos -->
text-sm, text-lg, text-xl   <!-- Font sizes -->
fw-bold, fw-semibold        <!-- Font weights -->
text-center, text-start     <!-- Text align -->
```

## 🔧 Padrões Comuns

### Hero Section
```html
<section class="hero-section">
  <div class="container-fluid">
    <h1 class="hero-title">Título</h1>
    <p class="hero-subtitle">Descrição</p>
  </div>
</section>
```

### Card Grid
```html
<div style="display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); 
            gap: 1.5rem;">
  <div class="card">Card 1</div>
  <div class="card">Card 2</div>
</div>
```

### Duas Colunas
```html
<div style="display: grid; 
            grid-template-columns: 1fr; 
            gap: 2rem;">
  <div>Coluna 1</div>
  <div>Coluna 2</div>
</div>

@media (min-width: 768px) {
  div { grid-template-columns: 1fr 1fr; }
}
```

### Sidebar + Main
```html
<div style="display: grid; 
            grid-template-columns: 1fr;">
  <aside>Sidebar</aside>
  <main>Conteúdo</main>
</div>

@media (min-width: 992px) {
  div { grid-template-columns: 250px 1fr; gap: 2rem; }
}
```

## 🚨 Armadilhas Comuns

### ❌ Evite
- [ ] `width: 100vw` (causa overflow)
- [ ] `position: fixed` em mobile (causa problemas)
- [ ] `width` em pixels em containers
- [ ] `padding/margin` muito grande em mobile
- [ ] Fontes muito pequenas (< 12px)
- [ ] Sem viewport meta tag
- [ ] Imagens não responsivas
- [ ] Touch targets < 44px
- [ ] Overflow horizontal

### ✅ Faça
- [ ] Use `max-width` em containers
- [ ] Prefira `position: relative`/`static`
- [ ] Use percentuais ou unidades relativas
- [ ] Escale espaçamento por breakpoint
- [ ] Font-size mínimo 14px
- [ ] Sempre viewport meta tag
- [ ] Use `max-width: 100%` em imagens
- [ ] Botões/links mín 44px x 44px
- [ ] Overflow auto/hidden quando necessário

## 📊 Checklist Final

### Antes de Deploy
- [ ] Testado em 5+ dispositivos reais
- [ ] DevTools responsive = OK
- [ ] Lighthouse score > 90
- [ ] Sem console errors
- [ ] Sem warnings de acessibilidade
- [ ] Mobile-first = funciona
- [ ] Desktop = otimizado
- [ ] Print = legível
- [ ] Dark mode = se implementado
- [ ] Performance = aceitável

### Documentação
- [ ] Template bem comentado
- [ ] Classes com sentido
- [ ] Breakpoints claros
- [ ] Padrões documentados
- [ ] Exemplos quando complexo

### Código Limpo
- [ ] CSS sem repetição
- [ ] Classes reutilizáveis
- [ ] Indentação correta
- [ ] Sem inline styles excessivos
- [ ] Mobile-first mindset

## 🎓 Referência Rápida

### Breakpoints
```
xs: 320px - 575px   (mobile)
sm: 576px - 767px   (mobile landscape)
md: 768px - 991px   (tablet)
lg: 992px - 1199px  (laptop)
xl: 1200px - 1399px (desktop)
xxl: 1400px+        (ultra-wide)
```

### Media Queries
```css
/* Mobile first */
.element { /* styles for mobile */ }

@media (min-width: 576px) { /* small */ }
@media (min-width: 768px) { /* medium */ }
@media (min-width: 992px) { /* large */ }
@media (min-width: 1200px) { /* xl */ }
@media (min-width: 1400px) { /* xxl */ }
```

### Imports CSS
```html
<!-- Responsivo base -->
<link rel="stylesheet" href="{% static 'usuario/css/responsive.css' %}">

<!-- Componentes -->
<link rel="stylesheet" href="{% static 'usuario/css/responsive-components.css' %}">

<!-- Avançado -->
<link rel="stylesheet" href="{% static 'usuario/css/responsive-advanced.css' %}">
```

---

## 📞 Recursos

- [MDN Responsive Design](https://developer.mozilla.org/pt-BR/docs/Learn/CSS/CSS_layout/Responsive_Design)
- `RESPONSIVIDADE.md` - Guia técnico
- `EXEMPLOS_RESPONSIVIDADE.md` - Exemplos práticos
- CSS comentado nos arquivos

---

**Versão**: 1.0
**Atualizado**: 29 de janeiro de 2026
**Status**: ✅ Completo

Bom coding! 🚀
