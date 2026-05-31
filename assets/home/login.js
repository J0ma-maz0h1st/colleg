document.addEventListener('DOMContentLoaded', () => {
    const loginModal = document.getElementById('login-modal');
    const openLoginBtn = document.getElementById('open-login-btn');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const loginForm = document.getElementById('login-form');
    const errorAlert = document.getElementById('login-error-alert');
    const submitBtn = document.getElementById('login-submit-btn');

    // Открытие модального окна

    if (openLoginBtn) {
        openLoginBtn.addEventListener('click', (e) => {
            e.preventDefault(); // На всякий случай гасим стандартное поведение ссылки
            loginModal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        });
    }

    // Закрытие модального окна
    const closeModal = () => {
        loginModal.classList.add('hidden');
        document.body.style.overflow = '';
        errorAlert.classList.add('hidden');
        loginForm.reset();
    };

    if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
    
    // Закрытие при клике на темную область вокруг окна
    window.addEventListener('click', (e) => {
        if (e.target === loginModal) closeModal();
    });

    // Обработка отправки формы (Авторизация)
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Собираем данные
            const usernameValue = document.getElementById('login-username').value.trim();
    const passwordValue = document.getElementById('login-password').value;
            
            // Очищаем прошлые ошибки и включаем лоадер-эффект на кнопке
            errorAlert.classList.add('hidden');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Авторизация...';

            try {
                const response = await fetch('/api/users/login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    // Отправляем гибридный объект. Поле ввода улетит и как email, и как username
                    body: JSON.stringify({ 
                        username: usernameValue, 
                        email: usernameValue, 
                        password: passwordValue 
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    // Железно синхронизируем ключи с дашбордом!
                    localStorage.setItem('jwt_access', data.access);
                    localStorage.setItem('jwt_refresh', data.refresh);
                    
                    // На всякий случай чистим старые переменные, чтобы не захламлять память
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');

                    // Переходим в рабочую область
                    window.location.href = '/home/';
                } else {
                    // Логируем в консоль точный ответ бэкенда, если опять будет 400
                    console.error("Ошибка авторизации от DRF:", data);
                    
                    // Сборщик текста ошибок для отображения в попапе
                    let errorMsg = 'Неверный логин или пароль';
                    if (data.detail) {
                        errorMsg = data.detail;
                    } else {
                        // Если прилетело 400 со списком ошибок полей (например, email: [...])
                        errorMsg = Object.entries(data).map(([key, val]) => `${key}: ${val}`).join(' | ');
                    }
                    throw new Error(errorMsg);
                }

            } catch (error) {
                // Выводим ошибку в наш неоновый алерт
                errorAlert.textContent = error.message;
                errorAlert.classList.remove('hidden');
            } finally {
                // Возвращаем кнопку в исходное состояние
                submitBtn.disabled = false;
                submitBtn.textContent = 'Войти';
            }
        });
    }
});