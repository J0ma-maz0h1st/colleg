document.addEventListener('DOMContentLoaded', async () => {
    const accessToken = localStorage.getItem('jwt_access');
    const logoutBtn = document.getElementById('logout-btn');
    const topbarLogoutBtn = document.getElementById('topbar-logout-btn');
    
    // Элементы меню и профиля
    const menuTrigger = document.getElementById('user-menu-trigger');
    const dropdownMenu = document.getElementById('topbar-dropdown');
    const topbarName = document.getElementById('topbar-user-name');
    const topbarAvatar = document.getElementById('topbar-user-avatar');
    
    const dropdownFullName = document.getElementById('dropdown-full-name');
    const dropdownRole = document.getElementById('dropdown-role');
    
    // Четкий выбор ссылок по ID
    const dropdownProfileLink = document.getElementById('dropdown-profile-link');
    const sidebarProfileLink = document.getElementById('sidebar-profile-link'); // Исправлено!

    // 1. Клиентская защита роута (Guard)
    if (!accessToken) {
        window.location.href = '/';
        return;
    }

    // Вспомогательная функция для декодирования JWT-токена
    function parseJwt(token) {
        try {
            return JSON.parse(atob(token.split('.')[1]));
        } catch (e) {
            return null;
        }
    }

    // 2. Инициализация данных пользователя
    const tokenData = parseJwt(accessToken);
    if (tokenData && tokenData.user_id) {
        try {
            const response = await fetch(`/api/users/profile/${tokenData.user_id}/`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const profileData = await response.json();
                
                // Формируем имя в тулбаре
                const fullName = `${profileData.first_name} ${profileData.last_name}`;
                if (topbarName) topbarName.textContent = profileData.first_name;
                if (dropdownFullName) dropdownFullName.textContent = fullName;
                
                if (dropdownRole) {
                    dropdownRole.textContent = profileData.gpa !== undefined ? 'Студент' : 'Преподаватель';
                }

                // Управляем аватаркой в тулбаре
                if (profileData.avatar && topbarAvatar) {
                    topbarAvatar.src = profileData.avatar;
                    topbarAvatar.classList.remove('hidden');
                }

                // Железно прописываем динамический URL в обе кнопки!
                const profileUrl = `/profile/${tokenData.user_id}/`;
                if (dropdownProfileLink) dropdownProfileLink.href = profileUrl;
                if (sidebarProfileLink) sidebarProfileLink.href = profileUrl;
                
                console.log(`Ссылки на профиль успешно сгенерированы: ${profileUrl}`);
            } else {
                console.error("Бэкенд вернул ошибку при запросе профиля:", response.status);
            }
        } catch (error) {
            console.error("Ошибка загрузки профиля:", error);
        }
    }

    // 3. Логика переключения дропдауна (GitHub style)
    if (menuTrigger && dropdownMenu) {
        menuTrigger.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdownMenu.classList.toggle('hidden');
        });

        document.addEventListener('click', () => {
            dropdownMenu.classList.add('hidden');
        });
    }

    // 4. Логика выхода
    const handleLogout = (e) => {
        e.preventDefault();
        localStorage.removeItem('jwt_access');
        localStorage.removeItem('jwt_refresh');
        window.location.href = '/';
    };

    if (logoutBtn) logoutBtn.addEventListener('click', handleLogout);
    if (topbarLogoutBtn) topbarLogoutBtn.addEventListener('click', handleLogout);
});