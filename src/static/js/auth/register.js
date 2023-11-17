document.getElementById("registerForm").addEventListener("submit", function(event) {
    event.preventDefault();

    var formData = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
        confirm_password: document.getElementById("confirm_password").value,
        name: document.getElementById("name").value,
        surname: document.getElementById("surname").value,
        patronymic: document.getElementById("patronymic").value,
        phone_number: document.getElementById("phone_number").value,
        // Другие поля
    };

    fetch('/pages/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Добавьте код для обработки успешной регистрации
    })
    .catch((error) => {
        console.error('Error:', error);
        // Добавьте код для обработки ошибки регистрации
    });
});