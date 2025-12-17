// ============================================
// DATA - FEATURED BOOKS
// ============================================
const featuredBooks = [
    {
        title: "Introdução à Inteligência Artificial",
        author: "Stuart Russell",
        category: "Tecnologia",
        rating: 5,
        available: true,
        coverColor: "cover-blue",
        categoryColor: "category-blue",
    },
    {
        title: "Fundamentos de Anatomia Humana",
        author: "Tortora & Derrickson",
        category: "Medicina",
        rating: 5,
        available: true,
        coverColor: "cover-red",
        categoryColor: "category-red",
    },
    {
        title: "Direito Constitucional Brasileiro",
        author: "José Afonso da Silva",
        category: "Direito",
        rating: 4,
        available: false,
        coverColor: "cover-amber",
        categoryColor: "category-amber",
    },
    {
        title: "Cálculo: Volume 1",
        author: "James Stewart",
        category: "Ciências Exatas",
        rating: 5,
        available: true,
        coverColor: "cover-green",
        categoryColor: "category-green",
    },
    {
        title: "Psicologia Social",
        author: "Aroldo Rodrigues",
        category: "Humanidades",
        rating: 4,
        available: true,
        coverColor: "cover-purple",
        categoryColor: "category-purple",
    },
    {
        title: "Química Orgânica",
        author: "Solomons & Fryhle",
        category: "Ciências Biológicas",
        rating: 4,
        available: false,
        coverColor: "cover-cyan",
        categoryColor: "category-cyan",
    },
    {
        title: "Administração de Empresas",
        author: "Idalberto Chiavenato",
        category: "Administração",
        rating: 5,
        available: true,
        coverColor: "cover-orange",
        categoryColor: "category-orange",
    },
    {
        title: "História da Arte",
        author: "E.H. Gombrich",
        category: "Artes",
        rating: 5,
        available: true,
        coverColor: "cover-pink",
        categoryColor: "category-pink",
    },
];

// ============================================
// DATA - CATEGORIES
// ============================================
const categories = [
    {
        name: "Ciências Exatas",
        icon: "book",
        count: 8500,
        color: "category-blue",
    },
    { name: "Medicina", icon: "book", count: 6200, color: "category-red" },
    { name: "Direito", icon: "book", count: 5800, color: "category-amber" },
    { name: "Tecnologia", icon: "book", count: 7400, color: "category-green" },
    {
        name: "Ciências Biológicas",
        icon: "book",
        count: 4300,
        color: "category-purple",
    },
    { name: "Artes", icon: "book", count: 2800, color: "category-pink" },
    { name: "Humanidades", icon: "book", count: 5100, color: "category-cyan" },
    { name: "Engenharias", icon: "book", count: 6900, color: "category-orange" },
];

// ============================================
// DATA - NEW ARRIVALS
// ============================================
const newBooks = [
    {
        title: "Machine Learning: Uma Abordagem Prática",
        author: "André Ng",
        date: "Nov 2024",
        category: "Tecnologia",
    },
    {
        title: "Neurociência Cognitiva",
        author: "Michael Gazzaniga",
        date: "Nov 2024",
        category: "Medicina",
    },
    {
        title: "Economia Comportamental",
        author: "Dan Ariely",
        date: "Out 2024",
        category: "Economia",
    },
    {
        title: "Física Quântica para Iniciantes",
        author: "Carlo Rovelli",
        date: "Out 2024",
        category: "Ciências Exatas",
    },
];

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Cria estrelas de classificação em HTML
 * @param {number} rating - Classificação de 1 a 5
 * @returns {string} HTML das estrelas
 */
function createStars(rating) {
    let stars = "";
    for (let i = 0; i < 5; i++) {
        if (i < rating) {
            stars += '<span class="material-symbols-outlined star">star</span>';
        } else {
            stars +=
                '<span class="material-symbols-outlined star" style="opacity: 0.3;">star</span>';
        }
    }
    return stars;
}

/**
 * Formata números para o padrão brasileiro
 * @param {number} num - Número a ser formatado
 * @returns {string} Número formatado
 */
function formatNumber(num) {
    return num.toLocaleString("pt-BR");
}

/**
 * Log com timestamp
 * @param {string} message - Mensagem a ser exibida
 */
function log(message) {
    console.log(`[${new Date().toLocaleTimeString("pt-BR")}] ${message}`);
}

// ============================================
// RENDER FEATURED BOOKS
// ============================================
function renderFeaturedBooks() {
    const container = document.getElementById("featured-books");

    if (!container) {
        console.error("Elemento featured-books não encontrado");
        return;
    }

    container.innerHTML = featuredBooks
        .map(
            (book, index) => `
    <article class="book-card" style="animation-delay: ${index * 0.05}s">
      <div class="book-cover ${book.coverColor}">
        <span class="material-symbols-outlined book-cover-icon">book</span>
        <button class="bookmark-btn" title="Adicionar aos favoritos" data-book-index="${index}">
          <i class="fa-regular fa-bookmark"></i>
        </button>
      </div>
      <div class="book-content">
        <h3 class="book-title">${escapeHtml(book.title)}</h3>
        <p class="book-author">${escapeHtml(book.author)}</p>
        <div class="book-meta">
          <span class="book-category">${escapeHtml(book.category)}</span>
          <div class="book-rating">
            ${createStars(book.rating)}
          </div>
        </div>
        <div style="margin-top: 1rem;">
          <span class="book-status ${book.available ? "status-available" : "status-unavailable"
                }">
            ${book.available ? "Disponível" : "Emprestado"}
          </span>
        </div>
      </div>
    </article>
  `
        )
        .join("");

    // Add bookmark functionality
    document.querySelectorAll(".bookmark-btn").forEach((btn) => {
        btn.addEventListener("click", handleBookmarkClick);
    });
}

/**
 * Handle bookmark button click
 * @param {Event} e - Evento do clique
 */
function handleBookmarkClick(e) {
    e.preventDefault();
    e.stopPropagation();

    const bookIndex = this.getAttribute("data-book-index");
    const book = featuredBooks[bookIndex];

    this.classList.toggle("active");

    if (this.classList.contains("active")) {
        log(`📌 "${book.title}" adicionado aos favoritos`);
    } else {
        log(`📌 "${book.title}" removido dos favoritos`);
    }
}

// ============================================
// RENDER CATEGORIES
// ============================================
function renderCategories() {
    const container = document.getElementById("categories");

    if (!container) {
        console.error("Elemento categories não encontrado");
        return;
    }

    container.innerHTML = categories
        .map(
            (cat, index) => `
    <a href="#" class="category-card" data-category-index="${index}" style="animation-delay: ${index * 0.05
                }s">
      <div class="category-icon ${cat.color}">
        <span class="material-symbols-outlined">${cat.icon}</span>
      </div>
      <h3 class="category-name">${escapeHtml(cat.name)}</h3>
      <p class="category-count">${formatNumber(cat.count)} títulos</p>
    </a>
  `
        )
        .join("");

    // Add click handlers
    document.querySelectorAll(".category-card").forEach((card) => {
        card.addEventListener("click", handleCategoryClick);
    });
}

/**
 * Handle category card click
 * @param {Event} e - Evento do clique
 */
function handleCategoryClick(e) {
    e.preventDefault();

    const categoryIndex = this.getAttribute("data-category-index");
    const category = categories[categoryIndex];

    log(`📚 Navegando para a categoria: ${category.name}`);

    // Simulando navegação (em produção, isso levaria a uma página de filtro)
    showToast(`Filtrando por: ${category.name}`);
}

// ============================================
// RENDER NEW ARRIVALS
// ============================================
function renderNewArrivals() {
    const container = document.getElementById("new-books");

    if (!container) {
        console.error("Elemento new-books não encontrado");
        return;
    }

    container.innerHTML = newBooks
        .map(
            (book, index) => `
    <div class="new-book-item" data-book-index="${index}" style="animation-delay: ${index * 0.1
                }s">
      <div class="book-icon-wrapper">
        <span class="material-symbols-outlined">book</span>
      </div>
      <div class="new-book-content">
        <h3 class="new-book-title">${escapeHtml(book.title)}</h3>
        <p class="new-book-author">${escapeHtml(book.author)}</p>
        <div class="new-book-meta">
          <span class="new-book-category">${escapeHtml(book.category)}</span>
          <span class="new-book-date">
            ${escapeHtml(book.date)}
          </span>
        </div>
      </div>
    </div>
  `
        )
        .join("");

    // Add click handlers
    document.querySelectorAll(".new-book-item").forEach((item) => {
        item.addEventListener("click", handleNewBookClick);
    });
}

/**
 * Handle new book item click
 * @param {Event} e - Evento do clique
 */
function handleNewBookClick(e) {
    const bookIndex = this.getAttribute("data-book-index");
    const book = newBooks[bookIndex];

    log(`📖 Abrindo detalhes de: ${book.title}`);
    showToast(`Detalhes de: ${book.title}`);
}

// ============================================
// MOBILE MENU
// ============================================
function setupMobileMenu() {
    const menuBtn = document.getElementById("mobile-menu-btn");
    const navbarCollapse = document.getElementById("navbarNav");
    const navLinks = navbarCollapse?.querySelectorAll(".nav-link");

    if (menuBtn) {
        menuBtn.addEventListener("click", function () {
            const isOpen = navbarCollapse.classList.contains("show");

            if (isOpen) {
                navbarCollapse.classList.remove("show");
                log("📱 Menu móvel fechado");
            } else {
                navbarCollapse.classList.add("show");
                log("📱 Menu móvel aberto");
            }
        });
    }

    // Close menu when link is clicked
    navLinks?.forEach((link) => {
        link.addEventListener("click", function () {
            navbarCollapse?.classList.remove("show");
        });
    });
}

// ============================================
// SEARCH FUNCTIONALITY
// ============================================
function setupSearch() {
    const searchBtn = document.getElementById("search-btn");
    const searchInput = document.querySelector(".hero-search .form-control");

    if (searchBtn) {
        searchBtn.addEventListener("click", function () {
            performSearch();
        });
    }

    if (searchInput) {
        searchInput.addEventListener("keypress", function (e) {
            if (e.key === "Enter") {
                performSearch();
            }
        });
    }
}

/**
 * Realiza a busca
 */
function performSearch() {
    const searchInput = document.querySelector(".hero-search .form-control");
    const query = searchInput?.value.trim();

    if (!query) {
        showToast("Por favor, digite um termo de busca");
        return;
    }

    log(`🔍 Buscando por: ${query}`);
    showToast(`Buscando por: "${query}"`);

    // Aqui você poderia filtrar os livros baseado na busca
    // filterBooks(query);
}

// ============================================
// YEAR IN FOOTER
// ============================================
function updateFooterYear() {
    const yearElement = document.getElementById("year");
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
}

// ============================================
// SMOOTH SCROLLING
// ============================================
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener("click", function (e) {
            const href = this.getAttribute("href");
            if (href === "#" || href === "") return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start",
                });

                // Log da navegação
                log(`📍 Navegando para: ${href}`);
            }
        });
    });
}

// ============================================
// TOAST NOTIFICATION
// ============================================

/**
 * Mostra uma notificação toast
 * @param {string} message - Mensagem a exibir
 * @param {string} type - Tipo: 'info', 'success', 'warning', 'error'
 * @param {number} duration - Duração em ms (padrão: 3000)
 */
function showToast(message, type = "info", duration = 3000) {
    // Criar elemento toast
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    // Estilos
    toast.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: ${getToastColor(type)};
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 0.5rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 9999;
    animation: slideInRight 0.3s ease-out;
    max-width: 300px;
    word-wrap: break-word;
    font-size: 0.9rem;
  `;

    document.body.appendChild(toast);

    // Remover após duração
    setTimeout(() => {
        toast.style.animation = "slideOutRight 0.3s ease-out";
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

/**
 * Retorna a cor baseada no tipo de toast
 * @param {string} type - Tipo de toast
 * @returns {string} Cor em hex
 */
function getToastColor(type) {
    const colors = {
        success: "#22c55e",
        error: "#ef4444",
        warning: "#f59e0b",
        info: "#3b82f6",
    };
    return colors[type] || colors["info"];
}

// Adicionar animações CSS
function addToastStyles() {
    const style = document.createElement("style");
    style.textContent = `
    @keyframes slideInRight {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
    
    @keyframes slideOutRight {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(400px);
        opacity: 0;
      }
    }
  `;
    document.head.appendChild(style);
}

// ============================================
// HELPER FUNCTIONS
// ============================================

/**
 * Escapa caracteres HTML especiais
 * @param {string} text - Texto a escapar
 * @returns {string} Texto escapado
 */
function escapeHtml(text) {
    const map = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;",
    };
    return text.replace(/[&<>"']/g, (m) => map[m]);
}

// ============================================
// INTERSECTION OBSERVER FOR LAZY LOADING
// ============================================
function setupIntersectionObserver() {
    const options = {
        threshold: 0.1,
        rootMargin: "0px 0px 50px 0px",
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                // Adicionar animação quando visível
                entry.target.style.opacity = "1";
                observer.unobserve(entry.target);
            }
        });
    }, options);

    // Observar cards
    document
        .querySelectorAll(".book-card, .category-card, .new-book-item")
        .forEach((card) => {
            observer.observe(card);
        });
}

// ============================================
// ERROR HANDLING
// ============================================
window.addEventListener("error", (event) => {
    console.error("Erro na aplicação:", event.error);
    showToast("Ocorreu um erro. Por favor, recarregue a página.", "error", 5000);
});

// ============================================
// INIT
// ============================================
document.addEventListener("DOMContentLoaded", function () {
    log("🚀 Iniciando Biblioteca Acadêmica...");

    try {
        // Adicionar estilos para toasts
        addToastStyles();

        // Renderizar conteúdo dinâmico
        renderFeaturedBooks();
        renderCategories();
        renderNewArrivals();

        // Setup funcionalidades
        setupMobileMenu();
        setupSearch();
        updateFooterYear();
        setupSmoothScroll();
        setupIntersectionObserver();

        log("✅ Biblioteca Acadêmica carregada com sucesso!");
        showToast("Bem-vindo à Biblioteca Acadêmica!", "success");
    } catch (error) {
        console.error("Erro durante inicialização:", error);
        showToast("Erro ao carregar a aplicação", "error");
    }
});

// ============================================
// PERFORMANCE MONITORING
// ============================================
if (window.performance && window.performance.timing) {
    window.addEventListener("load", function () {
        const perfData = window.performance.timing;
        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
        log(`⏱️ Tempo de carregamento: ${pageLoadTime}ms`);
    });
}
