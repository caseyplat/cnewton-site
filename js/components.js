/* Shared components for cnewton.org */

(function() {
    'use strict';

    // Navigation links configuration
    const NAV_LINKS = [
        { href: '/#bio', text: 'BIO', internal: true },
        { href: '/blog/', text: 'BLOG', internal: true },
        { href: 'https://bsky.app/profile/caseynewton.bsky.social', text: 'BLUESKY' },
        { href: 'https://www.threads.net/@crumbler', text: 'THREADS' },
        { href: 'https://www.linkedin.com/in/caseynewton1/', text: 'LINKEDIN' },
        { href: 'https://signal.me/#eu/JnqpZ8L9OdqPAacsZ4S7BTFjJh4P8EcqfMlsB9pjH9Ve-395dJdCpqbQjWwWGgOt', text: 'SIGNAL' }
    ];

    // Footer links configuration
    const FOOTER_LINKS = [
        { href: 'https://www.platformer.news/', text: 'PLATFORMER' },
        { href: 'https://www.nytimes.com/column/hard-fork', text: 'HARD FORK' },
        { href: 'mailto:casey@platformer.news', text: 'CONTACT' }
    ];

    // Get current path to determine active link
    const currentPath = window.location.pathname;

    /**
     * Renders the navigation bar
     * @param {Object} options - Configuration options
     * @param {boolean} options.fixed - Whether nav should be fixed position
     * @param {string} options.activePath - Path to mark as active (default: auto-detect)
     */
    window.renderNav = function(options = {}) {
        const navEl = document.getElementById('site-nav');
        if (!navEl) return;

        const fixed = options.fixed || false;
        const activePath = options.activePath || currentPath;

        const linksHtml = NAV_LINKS.map(link => {
            const isActive = link.internal && activePath.startsWith(link.href.replace('/#', '/').replace('#', '/'));
            const activeClass = isActive ? ' class="nav-active"' : '';
            const target = link.internal ? '' : ' target="_blank"';
            return `<a href="${link.href}"${activeClass}${target}>${link.text}</a>`;
        }).join('\n            ');

        navEl.className = fixed ? 'nav-fixed' : '';
        navEl.innerHTML = `
        <a href="/" class="logo">cnewton.org</a>
        <div class="nav-links">
            ${linksHtml}
            <button class="theme-toggle" id="theme-toggle" aria-label="Toggle theme">
                <span class="theme-toggle-text">MODE</span>
            </button>
        </div>
    `;

        // Initialize theme toggle after nav is rendered
        initThemeToggle();
    };

    /**
     * Initializes the theme toggle functionality
     */
    function initThemeToggle() {
        const themeToggle = document.getElementById('theme-toggle');
        if (!themeToggle) return;

        const html = document.documentElement;

        // Check for saved theme preference or system preference
        function getPreferredTheme() {
            const saved = localStorage.getItem('theme');
            if (saved) return saved;
            return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
        }

        // Apply theme
        function setTheme(theme) {
            html.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            const textEl = themeToggle.querySelector('.theme-toggle-text');
            if (textEl) {
                textEl.textContent = theme === 'light' ? 'DARK' : 'LIGHT';
            }
        }

        // Initialize theme
        setTheme(getPreferredTheme());

        // Toggle on click
        themeToggle.addEventListener('click', () => {
            const current = html.getAttribute('data-theme');
            setTheme(current === 'light' ? 'dark' : 'light');
        });

        // Listen for system preference changes
        window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                setTheme(e.matches ? 'light' : 'dark');
            }
        });
    }

    // Expose initThemeToggle globally for pages with static nav
    window.initThemeToggle = initThemeToggle;

    /**
     * Renders the footer
     * @param {Object} options - Configuration options
     * @param {boolean} options.extended - Whether to use extended footer style
     * @param {boolean} options.showLinks - Whether to show footer links (default: true for extended)
     */
    window.renderFooter = function(options = {}) {
        const footerEl = document.getElementById('site-footer');
        if (!footerEl) return;

        const extended = options.extended || false;
        const showLinks = options.showLinks !== undefined ? options.showLinks : extended;
        const year = new Date().getFullYear();

        footerEl.className = extended ? 'footer-extended' : '';

        let html = '';
        if (showLinks) {
            const linksHtml = FOOTER_LINKS.map(link =>
                `<a href="${link.href}" target="_blank" class="footer-link">${link.text}</a>`
            ).join('\n            ');
            html += `
        <div class="footer-links">
            ${linksHtml}
        </div>
    `;
        }

        html += `<p class="footer-copy">&copy; ${year} Casey Newton${extended ? ' <span>_</span>' : ''}</p>`;

        footerEl.innerHTML = html;
    };

    // Auto-initialize if elements exist
    document.addEventListener('DOMContentLoaded', function() {
        // Check for nav element with data attributes
        const navEl = document.getElementById('site-nav');
        if (navEl) {
            const fixed = navEl.dataset.fixed === 'true';
            const activePath = navEl.dataset.active || currentPath;
            renderNav({ fixed, activePath });
        }

        // Check for footer element with data attributes
        const footerEl = document.getElementById('site-footer');
        if (footerEl) {
            const extended = footerEl.dataset.extended === 'true';
            const showLinks = footerEl.dataset.links !== 'false';
            renderFooter({ extended, showLinks });
        }
    });
})();
