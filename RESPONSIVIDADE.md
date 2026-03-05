# Guia de Responsividade - Biblioteca Acadêmica

## 📱 Visão Geral

Este projeto implementa responsividade completa em todos os templates HTML usando um sistema robusto de CSS que garante uma experiência consistente em dispositivos de diferentes tamanhos.

## 🎯 Breakpoints Definidos

Os seguintes breakpoints foram definidos para guiar o design responsivo:

```css
--breakpoint-xs: 320px   /* Smartphone pequeno */
--breakpoint-sm: 576px   /* Smartphone grande */
--breakpoint-md: 768px   /* Tablet */
--breakpoint-lg: 992px   /* Laptop */
--breakpoint-xl: 1200px  /* Desktop */
--breakpoint-xxl: 1400px /* Desktop grande */
```

## 📂 Arquivos CSS Responsivos

### 1. `static/usuario/css/responsive.css`
- **Finalidade**: Sistema de grid, layout utilities, spacing utilities
- **Inclui**: 
  - Container fluid com padding responsivo
  - Grid system (12 colunas)
  - Display utilities (d-none, d-block, d-flex, etc.)
  - Flex utilities (flexbox helpers)
  - Spacing utilities (margin, padding)
  - Tipografia responsiva
  - Imagens responsivas
  - Aspect ratio helpers
  - Formulários responsivos
  - Botões responsivos

### 2. `static/usuario/css/responsive-components.css`
- **Finalidade**: Componentes específicos e patterns avançados
- **Inclui**:
  - Tabelas responsivas
  - Navbar responsiva
  - Card grids adaptáveis
  - Formulários com grid
  - Modais responsivos
  - Sidebars colapsáveis
  - Hero sections adaptáveis
  - Listas responsivas
  - Paginação responsiva
  - Badges e labels
  - Stat cards
  - Print styles

## 🔨 Como Usar as Utilidades

### Classes de Grid

```html
<!-- Grid com 12 colunas -->
<div class="row">
  <div class="col-12 col-md-6 col-lg-4">
    <!-- Ocupa 12 em mobile, 6 em tablets, 4 em desktops -->
  </div>
</div>
```

### Classes de Display

```html
<!-- Mostrar apenas em dispositivos grandes -->
<div class="d-none d-lg-block">
  Visible apenas em lg+
</div>

<!-- Flexbox responsivo -->
<div class="d-flex flex-column flex-md-row gap-3">
  Conteúdo flexível
</div>
```

### Classes de Spacing

```html
<!-- Margins responsivas -->
<div class="m-2 m-md-4">
  Margin responsiva
</div>

<!-- Padding -->
<div class="p-3 py-5">
  Padding responsivo
</div>
```

### Tipografia Responsiva

```html
<h1 class="h1">
  <!-- Escala automaticamente em móvel -->
  Título responsivo
</h1>

<p class="text-lg text-md-xl">
  <!-- Texto que aumenta em dispositivos maiores -->
</p>
```

## 📊 Padrões Responsivos Comuns

### 1. Container Fluid com Padding

```html
<div class="container-fluid">
  <!-- Padding: 1rem em xs/sm, 1.5rem em md, 2rem em lg, 3rem em xl -->
</div>
```

### 2. Grid Automático

```html
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
  <!-- Cards que se ajustam automaticamente -->
</div>
```

### 3. Navbar Responsiva

```html
<nav class="navbar">
  <div class="navbar-brand">Logo</div>
  <button class="navbar-toggler d-md-none">Menu</button>
  <div class="navbar-collapse d-none d-md-flex">
    <!-- Menu items -->
  </div>
</nav>
```

### 4. Hero Section

```html
<section class="hero-section">
  <!-- Ajusta padding e font-size em mobile -->
  <h1 class="hero-title">Título</h1>
  <p class="hero-subtitle">Descrição</p>
</section>
```

### 5. Tabelas Responsivas

```html
<!-- Em tablets/mobile, a tabela se converte em cards -->
<table>
  <tr>
    <td data-label="Nome">Valor</td>
  </tr>
</table>
```

## 🎨 Classes Úteis por Caso de Uso

### Para Cards/Grid

```html
<div class="cards-grid">
  <!-- Automatically responsive: 1 col em xs, 2 em sm, 3 em md, 4 em lg -->
</div>
```

### Para Formulários

```html
<div class="form-row">
  <!-- Grid responsivo para inputs -->
  <input class="form-control">
  <input class="form-control">
</div>
```

### Para Botões

```html
<div class="btn-group">
  <!-- Em mobile: coluna, em desktop: linha -->
  <button class="btn">Ação 1</button>
  <button class="btn">Ação 2</button>
</div>
```

### Para Listas

```html
<ul class="list-group">
  <li class="list-group-item">Item</li>
  <!-- Font size se ajusta em mobile -->
</ul>
```

## 📱 Checklist de Responsividade

Ao criar novos templates, certifique-se de:

- [ ] Incluir `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- [ ] Importar `responsive.css` e `responsive-components.css`
- [ ] Usar classes grid (`col-*`) ou `display: grid`
- [ ] Testar em dispositivos de diferentes tamanhos
- [ ] Usar `d-none`/`d-block` para esconder/mostrar elementos
- [ ] Aplicar classes de spacing responsivas
- [ ] Garantir que inputs tenham `width: 100%` em mobile
- [ ] Testar em orientação retrato e paisagem
- [ ] Validar performance em conexões lentas

## 🔍 Media Queries Personalizadas

Se precisar de CSS customizado além das utilidades, use os breakpoints definidos:

```css
/* Mobile First */
.my-element {
  padding: 1rem;
  font-size: 14px;
}

@media (min-width: 576px) {
  /* Small devices e acima */
  .my-element {
    padding: 1.5rem;
  }
}

@media (min-width: 768px) {
  /* Medium devices e acima */
  .my-element {
    padding: 2rem;
    font-size: 16px;
  }
}

@media (min-width: 992px) {
  /* Large devices e acima */
  .my-element {
    padding: 3rem;
  }
}
```

## 🚀 Boas Práticas

1. **Mobile First**: Sempre comece com o design móvel
2. **Proporções**: Use unidades relativas (rem, em, %)
3. **Flexibilidade**: Prefira grid/flexbox a floats
4. **Teste**: Use DevTools para testar diferentes resoluções
5. **Acessibilidade**: Mantenha bom contraste e tamanhos legíveis
6. **Performance**: Minimize CSS redundante
7. **Semântica**: Use nomes de classes descritivos

## 📚 Referências

- [MDN Web Docs - Responsive Design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [CSS Tricks - A Complete Guide to Grid](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [MDN - Flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout)

## ✅ Templates Atualizados

Os seguintes templates foram atualizados com responsividade:

- ✅ `templates/usuario/index.html` - Página inicial
- ✅ `templates/usuario/entrar.html` - Login
- ✅ `templates/livro/livros.html` - Acervo
- ✅ `templates/livro/listar_emprestimos.html` - Empréstimos
- ✅ `templates/livro/renovar_emprestimo.html` - Renovação
- ✅ `templates/livro/detalhar_livro.html` - Detalhes do livro
- ✅ `templates/livro/historico_emprestimos.html` - Histórico
- ✅ `templates/livro/detalhe_reserva.html` - Detalhes de reserva
- ✅ `templates/admin/dashboard-admin.html` - Dashboard admin
- ✅ Todos os templates herdados dos acima

## 🎓 Exemplos Práticos

### Exemplo 1: Hero Section Responsiva

```html
<section class="hero-section" style="padding: 2rem 1rem;">
  <div class="container-fluid">
    <div class="d-flex flex-column justify-content-center gap-3">
      <h1 class="hero-title">Bem-vindo</h1>
      <p class="hero-subtitle">Descrição...</p>
    </div>
  </div>
</section>
```

### Exemplo 2: Grid de Cards

```html
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1.5rem;">
  <div class="card">Card 1</div>
  <div class="card">Card 2</div>
  <div class="card">Card 3</div>
</div>
```

### Exemplo 3: Formulário Responsivo

```html
<div class="form-row">
  <div class="form-group">
    <label>Nome</label>
    <input class="form-control" type="text">
  </div>
  <div class="form-group">
    <label>Email</label>
    <input class="form-control" type="email">
  </div>
</div>
```

## 🆘 Suporte e Contribuições

Se você tiver sugestões ou encontrar problemas com responsividade, por favor:

1. Teste em dispositivos reais
2. Use o DevTools do navegador
3. Documente o problema
4. Propor uma solução

---

**Última atualização**: 29 de janeiro de 2026
