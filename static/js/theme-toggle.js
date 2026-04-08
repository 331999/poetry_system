/**
 * 主题切换功能
 * 支持浅色/深色模式切换，并保存用户偏好到 localStorage
 */

(function() {
    'use strict';

    // 获取主题切换按钮和 HTML 元素
    const themeToggle = document.getElementById('themeToggle');
    const themeToggleMenu = document.getElementById('themeToggleMenu');
    const html = document.documentElement;

    // 从 localStorage 获取保存的主题
    const savedTheme = localStorage.getItem('theme') || 'light';

    // 初始化主题
    function initTheme() {
        html.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    }

    // 更新主题图标
    function updateThemeIcon(theme) {
        if (!themeToggle) return;

        const icon = themeToggle.querySelector('i');
        if (theme === 'dark') {
            icon.className = 'fa fa-sun-o';
            themeToggle.title = '切换到浅色模式';
        } else {
            icon.className = 'fa fa-moon-o';
            themeToggle.title = '切换到深色模式';
        }
    }

    // 切换主题
    function toggleTheme() {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);

        // 触发自定义事件，供其他组件监听
        window.dispatchEvent(new CustomEvent('themechange', {
            detail: { theme: newTheme }
        }));
    }

    // 绑定点击事件
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
    if (themeToggleMenu) {
        themeToggleMenu.addEventListener('click', function(e) {
            e.preventDefault();
            toggleTheme();
        });
    }

    // 初始化
    initTheme();

    // 监听系统主题变化
    if (window.matchMedia) {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        mediaQuery.addEventListener('change', function(e) {
            // 只有当用户没有手动设置过主题时，才跟随系统
            if (!localStorage.getItem('theme')) {
                const theme = e.matches ? 'dark' : 'light';
                html.setAttribute('data-theme', theme);
                updateThemeIcon(theme);
            }
        });
    }
})();
