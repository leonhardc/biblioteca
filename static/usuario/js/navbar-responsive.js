// ============================================
// NAVBAR RESPONSIVE TOGGLE
// Gerencia o comportamento do menu móvel
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const navLinks = document.querySelectorAll('.nav-link');
    const userMenuBtn = document.querySelector('#user-menu-btn');
    const userMenu = document.querySelector('.user-menu');
    const userDropdown = document.querySelector('#user-dropdown');
    const navItems = document.querySelectorAll('.nav-item');

    // Toggle navbar menu on mobile
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function(e) {
            e.stopPropagation();
            navbarCollapse.classList.toggle('show');
            navbarToggler.setAttribute('aria-expanded', navbarCollapse.classList.contains('show'));
            
            // Close user dropdown when toggling navbar
            if (userMenu && userDropdown) {
                userMenu.classList.remove('active');
                userDropdown.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // Close navbar when a link is clicked
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Don't close if it's the user menu button
            if (!this.id || this.id !== 'user-menu-btn') {
                if (window.innerWidth < 768) {
                    navbarCollapse.classList.remove('show');
                    if (navbarToggler) {
                        navbarToggler.setAttribute('aria-expanded', 'false');
                    }
                }
            }
        });
    });

    // User menu dropdown toggle (desktop)
    if (userMenuBtn && userDropdown) {
        userMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            userMenu.classList.toggle('active');
            userMenuBtn.setAttribute('aria-expanded', userMenu.classList.contains('active'));
        });

        // Close dropdown when clicking on an item
        const dropdownItems = userDropdown.querySelectorAll('.dropdown-item');
        dropdownItems.forEach(item => {
            item.addEventListener('click', function() {
                userMenu.classList.remove('active');
                if (userMenuBtn) {
                    userMenuBtn.setAttribute('aria-expanded', 'false');
                }
            });
        });
    }

    // Highlight active nav item
    function updateActiveNav() {
        const currentPath = window.location.pathname;
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && currentPath.includes(href.replace(/\/$/, ''))) {
                link.classList.add('active');
                link.setAttribute('aria-current', 'page');
            } else {
                link.classList.remove('active');
                link.removeAttribute('aria-current');
            }
        });
    }

    // Initial active state
    updateActiveNav();

    // Close menus when clicking outside
    document.addEventListener('click', function(e) {
        // Close navbar collapse
        if (navbarCollapse && !navbarCollapse.contains(e.target) && !navbarToggler?.contains(e.target)) {
            navbarCollapse.classList.remove('show');
            if (navbarToggler) {
                navbarToggler.setAttribute('aria-expanded', 'false');
            }
        }

        // Close user dropdown
        if (userDropdown && userMenu && !userDropdown.contains(e.target) && !userMenuBtn?.contains(e.target)) {
            userMenu.classList.remove('active');
            if (userMenuBtn) {
                userMenuBtn.setAttribute('aria-expanded', 'false');
            }
        }
    });

    // Handle window resize - close mobile menu on desktop
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            if (window.innerWidth >= 768) {
                // Close mobile menu on desktop size
                if (navbarCollapse) {
                    navbarCollapse.classList.remove('show');
                    if (navbarToggler) {
                        navbarToggler.setAttribute('aria-expanded', 'false');
                    }
                }
            }
        }, 100);
    });

    // Keyboard navigation support
    document.addEventListener('keydown', function(e) {
        // Close menu on Escape key
        if (e.key === 'Escape') {
            if (navbarCollapse) {
                navbarCollapse.classList.remove('show');
                if (navbarToggler) {
                    navbarToggler.setAttribute('aria-expanded', 'false');
                    navbarToggler.focus();
                }
            }

            if (userDropdown && userMenu) {
                userMenu.classList.remove('active');
                if (userMenuBtn) {
                    userMenuBtn.setAttribute('aria-expanded', 'false');
                    userMenuBtn.focus();
                }
            }
        }
    });

    // Mobile menu swipe support (optional)
    let touchStartX = 0;
    let touchEndX = 0;

    document.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
    }, false);

    document.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, false);

    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;

        // Swiped right - close menu
        if (diff > swipeThreshold && navbarCollapse && navbarCollapse.classList.contains('show')) {
            navbarCollapse.classList.remove('show');
            if (navbarToggler) {
                navbarToggler.setAttribute('aria-expanded', 'false');
            }
        }
    }

    // Initialize ARIA attributes
    if (navbarToggler) {
        navbarToggler.setAttribute('aria-expanded', 'false');
        navbarToggler.setAttribute('aria-controls', 'navbarNav');
    }

    if (userMenuBtn) {
        userMenuBtn.setAttribute('aria-expanded', 'false');
        userMenuBtn.setAttribute('aria-haspopup', 'true');
    }

    if (navbarCollapse) {
        navbarCollapse.setAttribute('id', 'navbarNav');
    }
});
