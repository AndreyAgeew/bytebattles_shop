
document.addEventListener('DOMContentLoaded', function () {
    const logoutButton = document.getElementById('logoutButton');

    if (logoutButton) {
        logoutButton.addEventListener('click', function (event) {
            event.preventDefault();
            fetch('/auth/logout', {
                method: 'POST',
                credentials: 'same-origin', // Включение отправки куки в запросе
            })
            .then(response => {
                if (response.ok) {
                    // Обработка успешного выхода
                    window.location.href = '/pages/login';  // Перенаправление пользователя после выхода
                } else {
                    console.error('Ошибка выхода:', response.statusText);
                }
            })
            .catch(error => {
                console.error('Ошибка выхода:', error);
            });
        });
    }
});