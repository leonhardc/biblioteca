# Exemplos Práticos de Responsividade

## 🎨 Exemplos Comuns de Uso

### 1. Hero Section com Background

```html
<section class="hero-section" style="padding: 2rem 1rem;">
  <div class="container-fluid">
    <div class="d-flex flex-column justify-content-center" style="gap: 2rem;">
      <h1 class="hero-title">
        Bem-vindo à Biblioteca Acadêmica
      </h1>
      <p class="hero-subtitle">
        Explore nosso acervo de mais de 50 mil títulos
      </p>
      <div class="hero-search">
        <input type="text" class="form-control" 
               placeholder="Buscar livro...">
        <button class="btn btn-primary">
          <i class="fa-solid fa-search"></i>
        </button>
      </div>
      <!-- Stats em grid responsivo -->
      <div style="display: grid; 
                  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
                  gap: 1.5rem; margin-top: 2rem;">
        <div class="stat-item">
          <div class="stat-value">50.000+</div>
          <div class="stat-label">Livros</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">12.000+</div>
          <div class="stat-label">Leitores</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">45+</div>
          <div class="stat-label">Anos</div>
        </div>
      </div>
    </div>
  </div>
</section>
```

### 2. Navbar com Menu Responsivo

```html
<header class="header-backdrop">
  <div class="container-fluid">
    <nav class="navbar">
      <!-- Logo -->
      <a href="/" class="navbar-brand">
        <div class="logo-box">
          <i class="fa-solid fa-book"></i>
        </div>
        <div class="logo-text d-none d-sm-block">
          <h1>Biblioteca</h1>
          <p>Acadêmica</p>
        </div>
      </a>

      <!-- Mobile Menu Toggle -->
      <button class="navbar-toggler d-md-none">
        <span class="fa-solid fa-bars"></span>
      </button>

      <!-- Navigation Menu -->
      <div class="navbar-collapse d-none d-md-flex">
        <ul class="navbar-nav">
          <li><a class="nav-link" href="#acervo">Acervo</a></li>
          <li><a class="nav-link" href="#categorias">Categorias</a></li>
          <li><a class="nav-link" href="#novidades">Novidades</a></li>
        </ul>
      </div>

      <!-- User Actions -->
      <div class="navbar-actions d-none d-md-flex">
        <a href="/login" class="btn btn-outline-secondary">
          <i class="fa-solid fa-user"></i>
          Entrar
        </a>
      </div>
    </nav>
  </div>
</header>
```

### 3. Grid de Cards

```html
<!-- Automático: 1 coluna mobile, 2 tablet, 3 desktop, 4 desktop-lg -->
<div class="cards-grid" 
     style="display: grid; 
             grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
             gap: 1.5rem;">
  <div class="card">
    <div class="card-header">
      <h3>Livro 1</h3>
    </div>
    <p>Descrição...</p>
  </div>
  <div class="card">
    <div class="card-header">
      <h3>Livro 2</h3>
    </div>
    <p>Descrição...</p>
  </div>
  <!-- Mais cards aqui -->
</div>
```

### 4. Formulário Responsivo

```html
<form class="form-responsive">
  <!-- Campo duplo em desktop, simples em mobile -->
  <div style="display: grid;
              grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
              gap: 1rem;
              margin-bottom: 1rem;">
    <div class="form-group">
      <label for="nome">Nome Completo</label>
      <input type="text" id="nome" class="form-control">
    </div>
    <div class="form-group">
      <label for="email">E-mail</label>
      <input type="email" id="email" class="form-control">
    </div>
  </div>

  <!-- Campo triplo -->
  <div style="display: grid;
              grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
              gap: 1rem;
              margin-bottom: 1rem;">
    <div class="form-group">
      <label for="telefone">Telefone</label>
      <input type="tel" id="telefone" class="form-control">
    </div>
    <div class="form-group">
      <label for="cidade">Cidade</label>
      <input type="text" id="cidade" class="form-control">
    </div>
    <div class="form-group">
      <label for="estado">Estado</label>
      <input type="text" id="estado" class="form-control">
    </div>
  </div>

  <!-- Botões responsivos -->
  <div style="display: grid;
              grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
              gap: 1rem;">
    <button type="submit" class="btn btn-primary">
      Enviar
    </button>
    <button type="reset" class="btn btn-secondary">
      Limpar
    </button>
  </div>
</form>
```

### 5. Tabela Responsiva

```html
<div class="table-responsive">
  <table>
    <thead>
      <tr>
        <th>ID</th>
        <th>Nome</th>
        <th>Email</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td data-label="ID">1</td>
        <td data-label="Nome">João Silva</td>
        <td data-label="Email">joao@example.com</td>
        <td data-label="Status">
          <span class="badge badge-success">Ativo</span>
        </td>
      </tr>
    </tbody>
  </table>
</div>

<style>
  .table-responsive {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  @media (max-width: 768px) {
    table { display: block; width: 100%; }
    thead { display: none; }
    tr { 
      display: block;
      margin-bottom: 1rem;
      border: 1px solid #ddd;
      padding: 1rem;
    }
    td {
      display: block;
      text-align: right;
      padding-left: 50%;
      position: relative;
    }
    td:before {
      content: attr(data-label);
      position: absolute;
      left: 1rem;
      font-weight: bold;
    }
  }
</style>
```

### 6. Duas Colunas Responsivas

```html
<!-- Coluna única em mobile, duas colunas em tablet+  -->
<div style="display: grid;
            grid-template-columns: 1fr;
            gap: 2rem;">
  <style>
    @media (min-width: 768px) {
      .two-column { grid-template-columns: 1fr 1fr; }
    }
  </style>
  <div>
    <h2>Conteúdo Principal</h2>
    <p>Lorem ipsum...</p>
  </div>
  <aside>
    <h3>Barra Lateral</h3>
    <p>Informações complementares...</p>
  </aside>
</div>
```

### 7. Sidebar Colapsável

```html
<div style="display: grid;
            grid-template-columns: 1fr;">
  <style>
    @media (min-width: 768px) {
      .with-sidebar { 
        grid-template-columns: 250px 1fr;
        gap: 2rem;
      }
    }
  </style>
  
  <!-- Sidebar -->
  <aside class="sidebar">
    <nav>
      <ul>
        <li><a href="#home">Home</a></li>
        <li><a href="#about">Sobre</a></li>
        <li><a href="#contact">Contato</a></li>
      </ul>
    </nav>
  </aside>

  <!-- Main Content -->
  <main>
    <h1>Conteúdo Principal</h1>
    <p>Lorem ipsum...</p>
  </main>
</div>
```

### 8. Footer com Colunas Responsivas

```html
<footer class="footer-dark py-5">
  <div class="container-fluid">
    <!-- Grid responsivo: 1 coluna mobile, 2 tablet, 4 desktop -->
    <div style="display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 2rem;
                margin-bottom: 2rem;">
      
      <!-- Coluna 1: About -->
      <div>
        <h4>Sobre</h4>
        <p>Descrição da biblioteca...</p>
      </div>

      <!-- Coluna 2: Links -->
      <div>
        <h4>Links Rápidos</h4>
        <ul class="list-group">
          <li><a href="#">Acervo</a></li>
          <li><a href="#">Reservas</a></li>
          <li><a href="#">Conta</a></li>
        </ul>
      </div>

      <!-- Coluna 3: Contact -->
      <div>
        <h4>Contato</h4>
        <p>📧 biblioteca@email.com</p>
        <p>📞 (11) 3000-0000</p>
      </div>

      <!-- Coluna 4: Hours -->
      <div>
        <h4>Horários</h4>
        <p>Seg-Sex: 8h - 20h</p>
        <p>Sábado: 9h - 17h</p>
      </div>
    </div>

    <!-- Copyright -->
    <div class="border-top pt-4 text-center">
      <p class="text-muted">© 2026 Biblioteca Acadêmica</p>
    </div>
  </div>
</footer>
```

### 9. Botões Responsivos

```html
<!-- Inline em desktop, stacked em mobile -->
<div class="btn-group">
  <button class="btn btn-primary">
    <i class="fa-solid fa-save"></i>
    <span class="d-none d-sm-inline">Salvar</span>
  </button>
  <button class="btn btn-secondary">
    <i class="fa-solid fa-times"></i>
    <span class="d-none d-sm-inline">Cancelar</span>
  </button>
  <button class="btn btn-danger">
    <i class="fa-solid fa-trash"></i>
    <span class="d-none d-sm-inline">Deletar</span>
  </button>
</div>

<style>
  .btn-group {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  @media (max-width: 576px) {
    .btn-group {
      flex-direction: column;
    }
    .btn-group .btn {
      width: 100%;
    }
  }
</style>
```

### 10. Typography Fluida

```html
<h1 style="font-size: clamp(1.5rem, 4vw, 3rem);">
  Título que escala fluidamente
</h1>

<p style="font-size: clamp(0.9rem, 2vw, 1.1rem);">
  Parágrafo que se adapta ao tamanho da viewport
</p>

<style>
  .text-fluid {
    font-size: clamp(1rem, 2vw, 2rem);
  }
  
  .text-fluid-lg {
    font-size: clamp(1.5rem, 3vw, 3rem);
  }
  
  .text-fluid-sm {
    font-size: clamp(0.75rem, 1.5vw, 1rem);
  }
</style>
```

## 🔍 Classes Úteis Prontas

### Mostrar/Esconder por Dispositivo
```html
<!-- Mostrar apenas em lg+ -->
<div class="d-none d-lg-block">Desktop only</div>

<!-- Mostrar apenas em md -->
<div class="d-none d-md-block d-lg-none">Tablet only</div>

<!-- Mostrar apenas em mobile -->
<div class="d-block d-md-none">Mobile only</div>
```

### Spacing Responsivo
```html
<!-- Margin/padding automático -->
<div class="mb-responsive">Margin bottom responsivo</div>
<div class="p-responsive">Padding responsivo</div>
<div class="gap-responsive">Gap responsivo</div>
```

### Flexbox Responsivo
```html
<!-- Column em mobile, row em desktop -->
<div class="flex-responsive">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### Grid Automático
```html
<!-- Grid que se adapta automaticamente -->
<div class="grid-auto-responsive">
  <!-- Cards auto-fill -->
</div>

<div class="grid-auto-responsive-lg">
  <!-- Cards maiores auto-fill -->
</div>
```

---

## ✅ Checklist ao Implementar

- [ ] Incluir meta viewport
- [ ] Importar CSS responsivo
- [ ] Testar em mobile (< 576px)
- [ ] Testar em tablet (576px - 768px)
- [ ] Testar em desktop (> 768px)
- [ ] Validar touch points (44px min)
- [ ] Testar em landscape
- [ ] Verificar legibilidade
- [ ] Testar com screen reader
- [ ] Validar performance

---

**Última atualização**: 29 de janeiro de 2026
