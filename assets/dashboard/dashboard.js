document.addEventListener('DOMContentLoaded', () => {
    // Проверяем именно твой ключ jwt_access
    const accessToken = localStorage.getItem('jwt_access');
    const logoutBtn = document.getElementById('logout-btn');

    // 1. Клиентская защита роута (Guard)
    if (!accessToken) {
        window.location.href = '/';
        return;
    }

    // 2. Исправленная логика кнопки Выйти (Logout)
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Стираем именно те ключи, которые создали!
            localStorage.removeItem('jwt_access');
            localStorage.removeItem('jwt_refresh');
            
            // На всякий случай чистим старые вариации, если они были
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            
            // Редирект на лендинг
            window.location.href = '/';
        });
    }
});