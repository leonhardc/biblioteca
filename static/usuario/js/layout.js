// Mobile menu toggle and user dropdown
document.addEventListener('DOMContentLoaded', function() {
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const navbarCollapse = document.getElementById('navbarNav');
        const userMenuBtn = document.getElementById('user-menu-btn');
        const userDropdown = document.getElementById('user-dropdown');

        if (mobileMenuBtn && navbarCollapse) {
            mobileMenuBtn.addEventListener('click', function() {
                navbarCollapse.classList.toggle('show');
                this.classList.toggle('active');
            });
        }

        if (userMenuBtn && userDropdown) {
            userMenuBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                userDropdown.classList.toggle('show');
            });

            document.addEventListener('click', function() {
                userDropdown.classList.remove('show');
            });

            userDropdown.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        }
    });